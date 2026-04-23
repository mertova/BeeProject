import os
import unittest
from pathlib import Path

import cv2

from form_analysis import FormAnalysis


class FormAnalysisTest(unittest.TestCase):

    reference_path = None
    data_samples = None
    test_root_path = None
    output_path = None

    @classmethod
    def setUpClass(cls):
        cls.test_root_path = Path(os.getcwd()).parents[0]

        cls.output_path = cls.test_root_path / "resources/results/test_analysis/"
        cls.output_path.mkdir(parents=True, exist_ok=True)

        cls.data_samples = cls.test_root_path / "resources/form1/samples"
        if not cls.data_samples.exists():
            raise FileNotFoundError("No image, path " + cls.data_samples.absolute().as_posix() + " is incorrect")

        cls.reference_path = cls.test_root_path / "resources/form1/form1_reference.png"
        if not cls.reference_path.is_file():
            raise FileNotFoundError("No image, path " + cls.reference_path.absolute().as_posix())

    def test_analysis_form1(self):
        # set
        form_analysis = FormAnalysis(cv2.imread(self.reference_path.as_posix()), "sift")
        # run
        reference = form_analysis.extract(self.data_samples, 3, True, True)

        # test
        cv2.imshow("reference", reference.get_color())
        cv2.waitKey(0)

    def test_analysis_form1_only_pen_elimination(self):
        # set
        reference_img = cv2.imread(self.reference_path.as_posix())

        # run
        form_analysis = FormAnalysis(reference_img, "sift")
        reference = form_analysis.extract(None, 0, False, True)

        # test
        cv2.imshow("reference", reference.get_color())
        cv2.waitKey(0)

    def test_analysis_form1_transform(self):
        # set
        reference_img = cv2.imread(self.reference_path.as_posix())
        form_analysis = FormAnalysis(reference_img, "sift")

        # run
        reference = form_analysis.extract(self.data_samples, 3, True, False)

        # test
        cv2.imshow("reference", reference.get_color())
        cv2.waitKey(0)

    def test_analysis_form2(self):
        pass


if __name__ == '__main__':
    unittest.main()
    print('Done!')
