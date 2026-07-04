import argparse
import sys
from pathlib import Path


def _add_extract_subcommand(subparsers):
    p = subparsers.add_parser(
        'extract',
        help='Extract a clean template and table structure from sample scans'
    )
    p.add_argument('-d', '--dataset', required=True, metavar='DIR',
                   help='Directory of sample scan images (.png)')
    p.add_argument('-r', '--reference', required=True, metavar='FILE',
                   help='Path to a representative reference image')
    p.add_argument('-o', '--output', default='./resources/data/extraction', metavar='DIR',
                   help='Output directory (default: ./resources/data/extraction)')
    p.add_argument('-ev', '--eps-v', type=int, default=15, metavar='N',
                   help='Epsilon for vertical grid lines (default: 15)')
    p.add_argument('-eh', '--eps-h', type=int, default=20, metavar='N',
                   help='Epsilon for horizontal grid lines (default: 20)')
    p.add_argument('-l', '--limit', type=int, default=15, metavar='N',
                   help='Max sample images to use (default: 15)')
    p.add_argument('-a', '--algo', choices=['sift', 'orb'], default='sift',
                   help='Feature matching algorithm (default: sift)')
    p.add_argument('--transform', action=argparse.BooleanOptionalAction, default=True,
                   help='Align samples to reference image (default: on)')
    p.add_argument('--averaging', action=argparse.BooleanOptionalAction, default=True,
                   help='Enable pen elimination via averaging (default: on)')


def _add_digitize_subcommand(subparsers):
    p = subparsers.add_parser(
        'digitize',
        help='Run OCR digitization on a dataset of filled forms'
    )
    p.add_argument('-d', '--dataset', required=True, metavar='DIR',
                   help='Directory of filled form images (.png)')
    p.add_argument('-o', '--output', required=True, metavar='DIR',
                   help='Output directory for digitized JSON results')
    p.add_argument('-s', '--service', choices=['google', 'azure', 'aws', 'tesseract'], default='google',
                   help='OCR backend to use (default: google)')
    p.add_argument('-c', '--credentials', default=None, metavar='FILE',
                   help='Path to OCR credentials .json file (not needed for --service tesseract)')
    p.add_argument('-t', '--table', required=True, metavar='FILE',
                   help='Path to table definition .json from the extract step')
    p.add_argument('-a', '--algo', choices=['sift', 'orb'], default='sift',
                   help='Feature matching algorithm used to align scans to the template '
                        '(must match the --algo used for bee extract; default: sift)')
    p.add_argument('--no-transform', action='store_true', default=False,
                   help='Skip image alignment to reference')
    p.add_argument('-D', '--debug', action='store_true', default=False,
                   help='Save intermediate images for debugging')


def _run_extract(args):
    import cv2
    from form_analysis import FormAnalysis
    from tsr import Tsr

    data_path = Path(args.dataset)
    if not data_path.is_dir():
        print(f"error: dataset directory not found: {data_path}", file=sys.stderr)
        return 1

    ref_path = Path(args.reference)
    if not ref_path.is_file():
        print(f"error: reference file not found: {ref_path}", file=sys.stderr)
        return 1

    out_path = Path(args.output)
    out_path.mkdir(parents=True, exist_ok=True)

    ref_image = cv2.imread(ref_path.as_posix())
    if ref_image is None:
        print(f"error: could not load reference image: {ref_path}", file=sys.stderr)
        return 1

    print("Extracting template ...")
    analyser = FormAnalysis(ref_image, args.algo)
    template = analyser.extract(data_path, args.limit, transform=args.transform, pen_elimination=args.averaging)

    if template is None:
        print("error: template extraction failed", file=sys.stderr)
        return 1

    template_path = out_path / 'template.png'
    cv2.imwrite(template_path.as_posix(), template.get_color())
    print(f"Template saved to {template_path}")

    print("Extracting table structure ...")
    tsr = Tsr(template_path, args.eps_h, args.eps_v, out_dir=out_path)
    tsr.extract()
    print(f"Table saved to {out_path / 'table.json'}")
    return 0


def _run_digitize(args):
    import json
    import cv2
    from digitize import Digitize
    from image_processing.reference import Reference
    from table.table import Table

    dataset_path = Path(args.dataset)
    if not dataset_path.is_dir():
        print(f"error: dataset directory not found: {dataset_path}", file=sys.stderr)
        return 1

    cred_path = None
    if args.service != 'tesseract':
        if args.credentials is None:
            print(f"error: --credentials is required for --service {args.service}", file=sys.stderr)
            return 1
        cred_path = Path(args.credentials)
        if not cred_path.is_file() or cred_path.suffix != '.json':
            print(f"error: credentials file not found or not .json: {cred_path}", file=sys.stderr)
            return 1

    table_path = Path(args.table)
    if not table_path.is_file() or table_path.suffix != '.json':
        print(f"error: table file not found or not .json: {table_path}", file=sys.stderr)
        return 1

    out_path = Path(args.output)
    out_path.mkdir(parents=True, exist_ok=True)

    with open(table_path, 'r') as f:
        table = Table()
        table.import_json(json.load(f))

    template_image = cv2.imread(table.template_path)
    if template_image is None:
        print(f"error: could not load template image: {table.template_path}", file=sys.stderr)
        return 1
    template = Reference(template_image, args.algo)
    debug_dir = out_path / 'debug' if args.debug else None
    intervals = [('F3', 'I35')]

    digitizer = Digitize(table, template, intervals, args.service, cred_path, debug_dir,
                        transform=not args.no_transform)

    digitalized_records = {}
    for x in sorted(dataset_path.glob('**/*.png')):
        if x.is_file():
            image_id = x.stem.split('_')[4]
            print(f"Processing {x.name}")
            annotations = digitizer.run(x, image_id)
            record_id = image_id.split('-')[1]
            digitalized_records[record_id] = annotations

    out_file = out_path / f"out_{dataset_path.stem}.json"
    with open(out_file, 'w') as f:
        json.dump(digitalized_records, f, sort_keys=True, indent=4)
    print(f"Results saved to {out_file}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog='bee',
        description='BeeProject - digitization of tabular forms from scanned images'
    )
    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    subparsers.required = True

    _add_extract_subcommand(subparsers)
    _add_digitize_subcommand(subparsers)

    args = parser.parse_args()

    if args.command == 'extract':
        sys.exit(_run_extract(args))
    elif args.command == 'digitize':
        sys.exit(_run_digitize(args))


if __name__ == '__main__':
    main()
