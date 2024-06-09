import unittest
from pathlib import Path

import cv2

import execute_extraction
from form_analysis import FormAnalysis


class IdentificationTest(unittest.TestCase):

    def test_analysis_form1(self):
        # set
        data_samples = Path('./scans/Niedersach_examples_10/')
        reference_path = Path('./scans/Niedersach_examples_10/Sample_Niedersachsen-2-1.png')
        output_path = Path('./results/5/')
        output_path.mkdir(parents=True, exist_ok=True)

        # run
        reference = cv2.imread(reference_path.as_posix())
        t = type(reference)
        form_analysis = FormAnalysis(output_path, reference)
        form_analysis.extract(data_samples, 5, True, True, True)

        # test
        results_dir = output_path / 'debug' / 'templates'
        p = results_dir.glob('**/*.png')
        i = 0
        for x in p:
            self.assertTrue(x.is_file())
            cv2.imshow(x.name, cv2.imread(x.as_posix()))
            cv2.waitKey(0)
            i += 1

    def test_analysis_form1_noTransform_noDebug(self):
        # set
        data_samples = Path('./scans/Niedersach_transformed_10/')
        reference_path = Path('./scans/Niedersach_examples_10/Sample_Niedersachsen-2-1.png')
        output_path = Path('./results/5/')
        output_path.mkdir(parents=True, exist_ok=True)

        # run
        reference = cv2.imread(reference_path.as_posix())
        t = type(reference)
        form_analysis = FormAnalysis(output_path, reference)
        form_analysis.extract(data_samples, 5, False, False, True)

        # test
        results_dir = output_path / 'templates'
        p = results_dir.glob('**/*.png')
        i = 0
        for x in p:
            self.assertTrue(x.is_file())
            self.assertTrue(x.name == 'mask.png')
            i += 1

    def test_analysis_form2(self):
        # set
        data_samples = Path('./scans/Form2-examples-51-png/')
        reference_path = Path('./scans/Niedersach_examples_10/Sample_Niedersachsen-2-1.png')
        output_path = Path('./results/5/')
        output_path.mkdir(parents=True, exist_ok=True)

        # run
        reference = cv2.imread(reference_path.as_posix())
        t = type(reference)
        form_analysis = FormAnalysis(output_path, reference)
        form_analysis.extract(data_samples, 5, True, True, True)

        # test
        results_dir = output_path / 'debug' / 'templates'
        p = results_dir.glob('**/*.png')
        i = 0
        for x in p:
            self.assertTrue(x.is_file())
            cv2.imshow(x.name, cv2.imread(x.as_posix()))
            cv2.waitKey(0)
            i += 1

    def test_analysis(self):
        data_samples = Path('./scans/Niedersach_examples_10/').as_posix()
        reference = Path('./scans/Niedersach_examples_10/Sample_Niedersachsen-2-1.png').as_posix()
        output_path = Path('./results/1/')
        output_path.mkdir(parents=True, exist_ok=True)
        template, grid = execute_extraction.main(path_t_output=output_path.as_posix(), path_reference=reference,
                                                 eps_h=20, eps_v=15, template_extraction=True,
                                                 path_data_sample=data_samples, data_limit=15, transform=True,
                                                 debug=True)
        self.assertIsNotNone(template)
        self.assertIsNotNone(grid)
        print(template)
        print(grid)

    def test_no_table_extraction(self):
        reference = Path('../data/form1/form1-manual-clean.png').as_posix()
        output_path = Path('./results/2/')
        output_path.mkdir(parents=True, exist_ok=True)
        grid = execute_extraction.main(path_t_output=output_path.as_posix(), path_reference=reference,
                                       eps_h=10, eps_v=20, template_extraction=False,
                                       debug=True)
        self.assertIsNotNone(grid)
        print(grid)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
