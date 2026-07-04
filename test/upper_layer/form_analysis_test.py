import unittest
from pathlib import Path

import cv2

from form_analysis import FormAnalysis

REPO_ROOT = Path(__file__).resolve().parents[2]


class FormAnalysisTest(unittest.TestCase):

    reference_path = None
    data_samples = None
    output_path = None

    @classmethod
    def setUpClass(cls):
        cls.output_path = REPO_ROOT / "test" / "results" / "form_analysis"
        cls.output_path.mkdir(parents=True, exist_ok=True)

        cls.data_samples = REPO_ROOT / "test" / "resources" / "form1" / "samples"
        if not cls.data_samples.exists():
            raise FileNotFoundError("No image, path " + cls.data_samples.absolute().as_posix() + " is incorrect")

        cls.reference_path = REPO_ROOT / "test" / "resources" / "form1" / "form1_reference.png"
        if not cls.reference_path.is_file():
            raise FileNotFoundError("No image, path " + cls.reference_path.absolute().as_posix())

    def test_analysis_form1(self):
        # set
        form_analysis = FormAnalysis(cv2.imread(self.reference_path.as_posix()), "sift")
        # run
        reference = form_analysis.extract(self.data_samples, 3, True, True)

        # test
        self.assertIsNotNone(reference)
        cv2.imwrite((self.output_path / "form1.png").as_posix(), reference.get_color())

    def test_analysis_form1_only_pen_elimination(self):
        # set
        reference_img = cv2.imread(self.reference_path.as_posix())

        # run
        form_analysis = FormAnalysis(reference_img, "sift")
        reference = form_analysis.extract(None, 0, False, False)

        # test
        self.assertIsNotNone(reference)
        cv2.imwrite((self.output_path / "form1_pen_elimination.png").as_posix(), reference.get_color())

    def test_analysis_form1_transform(self):
        # set
        reference_img = cv2.imread(self.reference_path.as_posix())
        form_analysis = FormAnalysis(reference_img, "sift")

        # run
        reference = form_analysis.extract(self.data_samples, 3, True, False)

        # test
        self.assertIsNotNone(reference)
        cv2.imwrite((self.output_path / "form1_transform.png").as_posix(), reference.get_color())


if __name__ == '__main__':
    unittest.main()
    print('Done!')
