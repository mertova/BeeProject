import argparse
import json
from pathlib import Path

from digitize import Digitize
from image_processing.form import Form
from src.table.table import Table


def main(dataset_path: Path, output_path: Path, credentials_json: Path, table_json: Path, regions: list[tuple]):
    with open(table_json.as_posix(), 'r') as f:
        table = Table()
        table.import_json(json.load(f))
        template = Form(table.template_path)

    p = dataset_path.glob('**/*.png')
    digitalized_records = {}
    for x in p:
        if x.is_file():
            image_id = x.stem.split('_')[4]
            print("Processing image ", image_id)
            digitize = Digitize(table, template, intervals, credentials_json, output_path, d)
            annotations = digitize.run(x, image_id)
            record_id = image_id.split("-")[1]
            digitalized_records[record_id] = annotations
    json.dump(digitalized_records, open(output_path.as_posix() + "/out_" + dataset_path.stem + ".json", 'w'),
              sort_keys=True, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='The BeeProject',
                                     description='Digitization of the tabular forms from the image. ',
                                     epilog='Process of OCR recognition on images')
    parser.add_argument("-resources", "--path_dataset", type=str, required=True,
                        help="Path to the dataset which should be digitized")
    parser.add_argument("-out", "--path_output", type=str, required=True,
                        help="Path to the output file for storing template")
    parser.add_argument("-cred", "--path_credentials", type=str, required=True,
                        help="Path to the OCR credentials .json file")
    parser.add_argument("-classes", "--table_file", type=str, required=True,
                        help="Path to the classes region definition .json file")

    parser.add_argument("-d", "--debug", action=argparse.BooleanOptionalAction, default=False,
                        help="debug mode activated")

    args = parser.parse_args()
    data_dir = Path(args.path_dataset)
    out_dir = Path(args.path_output)
    cred_dir = Path(args.path_credentials)
    table_dir = Path(args.table_file)
    d = args.debug
    intervals = [('F3', 'I35')]

    if not data_dir.exists():
        print("Dataset path does not exist")
        raise SystemExit(1)

    if not out_dir.exists():
        print("Output path does not exist, creating \"" + out_dir.as_posix() + "\" directory")

    if not cred_dir.is_file() or cred_dir.suffix != '.json':
        print("Json credentials file does not exist")
        raise SystemExit(1)

    if not table_dir.is_file() or table_dir.suffix != '.json':
        print("Json classes file does not exist")
        raise SystemExit(1)

    main(data_dir, out_dir, cred_dir, table_dir, intervals)


