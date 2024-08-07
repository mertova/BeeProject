import unittest
from pathlib import Path

import cv2

from form_analysis import FormAnalysis


class IdentificationTest(unittest.TestCase):
    def test_analysis_form1(self):
        # set
        data_samples = Path('C://Users//lmert//PhD//BeeProject/BeeProject/test/scans/form1-samples-2014')

        reference_path = Path('C://Users//lmert//PhD//BeeProject//BeeProject//data//form1//reference.png')
        # edit if new results should be generated
        output_path = Path('./results/9/')
        output_path.mkdir(parents=True, exist_ok=True)
        reference = cv2.imread(reference_path.as_posix())

        # run
        form_analysis = FormAnalysis(output_path, reference)
        form_analysis.extract(data_samples, 30, True, True, True)

        # test
        results_dir = output_path / 'debug' / 'templates'
        p = results_dir.glob('**/*.png')
        i = 0
        for x in p:
            self.assertTrue(x.is_file())
            cv2.imshow(x.name, cv2.imread(x.as_posix()))
            cv2.waitKey(0)
            i += 1

    def test_analysis_form1_only_pen_elimination(self):
        # set
        reference_path = Path('C://Users//lmert//PhD//BeeProject//BeeProject//data//form1//131.png')
        reference = cv2.imread(reference_path.as_posix())

        # edit if new results should be generated
        output_path = Path('./results/10-pen_eliminated/')
        output_path.mkdir(parents=True, exist_ok=True)

        # run
        form_analysis = FormAnalysis(output_path, reference)
        form_analysis.extract(None, 0, True, False, False)

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
        data_samples = Path('./scans/form1Samples/')
        reference_path = Path("C://Users//lmert//PhD//BeeProject//BeeProject//data//form1//template.png")
        # edit if new results should be generated
        output_path = Path('./results/8/')
        output_path.mkdir(parents=True, exist_ok=True)

        # run
        reference = cv2.imread(reference_path.as_posix())
        t = type(reference)
        form_analysis = FormAnalysis(output_path, reference)
        form_analysis.extract(data_samples, 20, True, True, True)

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
        reference_path = Path('./scans/Form2-examples-51/Sample_Form2-1.png')
        output_path = Path('./results/7/')
        output_path.mkdir(parents=True, exist_ok=True)

        # run
        reference = cv2.imread(reference_path.as_posix())
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


if __name__ == '__main__':
    unittest.main()
    print('Done!')
