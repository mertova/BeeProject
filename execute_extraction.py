import argparse
from pathlib import Path

from extraction.grid import Grid
from extraction.grid_extraction import GridExtraction
from extraction.template import Template
from extraction.template_extraction import TemplateExtraction


def main(path_t_output: str, path_reference: str, eps_h: int, eps_v: int, template_extraction: bool = False,
         path_data_sample: str = None, data_limit: int = None,
         transform: bool = False, debug: bool = False) -> tuple[Template, Grid]:
    out_dir = Path(path_t_output)
    if not out_dir.exists():
        print("The output directory doesn't exist.\n")
        raise exit(1)

    reference_dir = Path(path_reference)
    if not reference_dir.is_file():
        print("The path to the reference file is not valid or doesn't exist.\n")
        raise exit(1)

    t_extr = TemplateExtraction(out_dir, reference_dir)
    if template_extraction:
        print("Processing with template extraction ... ")
        data_sample_dir = Path(path_data_sample)
        if not data_sample_dir.exists():
            print("The data_sample directory doesn't exist.")
            raise exit(1)

        # extract template
        template = t_extr.extract(data_sample_dir, data_limit, transform=transform, debug=debug)
        template.dump_template()
    else:
        template = t_extr.get_template_from_reference()

    if template is None:
        print("Template not found")
        exit(1)

    # todo type check of eps
    g_extr = GridExtraction(out_dir, eps_h, eps_v, template=template)
    grid = g_extr.extract(debug)
    grid.export_json(out_dir)
    return template, grid


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='The BeeProject - Extract Templates',
                                     description='Digitization of the tabular forms from the image. Extracting empty '
                                                 'clean template file from the batch of handwritten filled images.')

    parser.add_argument("-out", "--path_t_output", type=str, required=True,
                        help="Path to the output file for storing template")

    parser.add_argument("-ref", "--path_reference", type=str, required=True,
                        help="Path to the template or reference file if we process template extraction")
    parser.add_argument("-data", "--path_data_sample", type=str, required=False,
                        help="Path to the data sample file")
    parser.add_argument("-template", "--template_extraction", action=argparse.BooleanOptionalAction,
                        default=False, help="Proceed with the template extraction")

    parser.add_argument("-ev", "--epsilon_vertical", type=int, required=True,
                        help="Epsilon - deviation for a vertical grid lines")
    parser.add_argument("-eh", "--epsilon_horizontal", type=int, required=True,
                        help="Epsilon - deviation for a horizontal grid lines")

    parser.add_argument("-t", "--transform", action=argparse.BooleanOptionalAction, default=False,
                        help="if true - proceed with alignment of sample data to the reference file")
    parser.add_argument("-d", "--debug", action=argparse.BooleanOptionalAction, default=False,
                        help="debug mode activated")
    args = parser.parse_args()

    main(args.path_t_output, args.eh, args.ev, args.path_reference, args.path_data_sample, args.template_extraction,
         args.transform, args.debug)
