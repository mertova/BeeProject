import argparse
from pathlib import Path

import cv2

from table.table import Table
from tsr import Tsr
from image_processing.reference import Reference
from form_analysis import FormAnalysis


def main(data_dir: str, ref_dir: str, eps_v: int = 15, eps_h: int = 20, data_limit: int = 15, transform: bool = True,
         out_dir: str = "./resources/data/extraction", averaging: bool = True) -> tuple[Reference, Table]:
    if type(eps_v) is not int or type(eps_h) is not int:
        raise TypeError('eps_v and eps_h must be integers')

    data_path = Path(data_dir)
    if not data_path.exists() or not data_path.is_dir():
        raise NotADirectoryError(data_path)

    ref_path = Path(ref_dir)
    if not ref_path.is_file():
        raise FileNotFoundError("The path to the reference file is not valid or doesn't exist.\n")
    ref_image = cv2.imread(ref_path.as_posix())

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    t_extr = FormAnalysis(ref_image)

    print("Processing with template extraction ... ")
    template = t_extr.extract(data_path, data_limit, transform=transform, pen_elimination=averaging)

    if template is None:
        print("Template not found")
        exit(1)
    else:
        template_path = (out_path / 'template.png').as_posix()
        print("Successfully extracted template, printing to " + template_path)
        cv2.imwrite(template_path, template.get_color())

    # todo type check of eps
    print("Processing with table extraction ... ")
    g_extr = Tsr(out_path, eps_h, eps_v, template=template)
    grid = g_extr.extract()
    grid.export_dict(out_path)
    return grid


if __name__ == '__main__':
    """
    This is the entry point of the table extraction."""
    # todo change ev and eh
    parser = argparse.ArgumentParser(prog='The BeeProject - Extract Templates',
                                     description='Digitization of the tabular forms from the image. Extracting empty '
                                                 'clean template file from the batch of handwritten filled images.')
    parser.add_argument("-d", "--dataset", type=str, required=True,
                        help="Path to the dataset")
    parser.add_argument("-r", "--reference", type=str, required=True,
                        help="Path to the representative image")
    parser.add_argument("-ev", "--eps_v", type=int, default=15,
                        help="Epsilon - deviation for a vertical grid lines")
    parser.add_argument("-eh", "--eps_h", type=int, default=15,
                        help="Epsilon - deviation for a horizontal grid lines")
    parser.add_argument("-l", "--limit", type=int, default=15,
                        help="Limit the sample files for table extraction")
    parser.add_argument("-t", "--transform", action=argparse.BooleanOptionalAction, default=True,
                        help="Transformation (alignment) of sample resources to the reference file")
    parser.add_argument("-o", "--output", type=str, default="./resources/data/extraction/",
                        help="Path to the output folder")
    args = parser.parse_args()

    main(args.dataset, args.reference, args.eps_v, args.eps_h, args.limit, args.transform, args.output)
