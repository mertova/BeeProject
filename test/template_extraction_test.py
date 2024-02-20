from pathlib import Path

import execute_template_extraction


def template_extraction():
    data_samples = Path('./scans/Niedersach_examples_10/')
    reference = Path("./scans/Niedersach_examples_10/Sample_Niedersachsen-2-1.png")
    output_path = Path('./')
    output_path.mkdir(parents=True, exist_ok=True)

    pen_elimination = True
    transform = True
    execute_template_extraction.main(reference.absolute(), data_samples.absolute(), output_path.absolute(),
                                     transform, pen_elimination, True)


def template_extraction_no_transform():
    data_samples = Path('./debug/template/transformed/')
    reference = Path("./scans/Niedersach_examples_10/Sample_Niedersachsen-2-1.png")
    output_path = Path('./')
    output_path.mkdir(parents=True, exist_ok=True)

    pen_elimination = True
    transform = False
    execute_template_extraction.main(reference.absolute(), data_samples.absolute(), output_path.absolute(),
                                     pen_elimination, transform, True)


if __name__ == '__main__':
    template_extraction()
    template_extraction_no_transform()
    print('Done!')
