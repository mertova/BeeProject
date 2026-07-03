import unittest
from pathlib import Path

import cv2
import numpy as np

from image_processing.image import Image

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestImage(unittest.TestCase):
    """
    Tests Image class
    """

    nparray_color = None
    out_path = None
    sample_img_path = None
    test_root_path = REPO_ROOT / "test"

    @classmethod
    def setUpClass(cls):
        cls.out_path = REPO_ROOT / "test" / "results" / "test_image"
        cls.out_path.mkdir(parents=True, exist_ok=True)

        cls.sample_img_path = REPO_ROOT / "test" / "resources" / "form1" / "samples" / "1.png"
        if not cls.sample_img_path.is_file():
            raise FileNotFoundError("No image, path " + cls.sample_img_path.absolute().as_posix() + " is incorrect")

        cls.nparray_color = cv2.imread(cls.sample_img_path.as_posix())
        cls.nparray_grey = cv2.cvtColor(cls.nparray_color, cv2.COLOR_BGR2GRAY)

    def test_init_color(self):
        image = Image(self.nparray_color)
        # test
        self.assertTrue(np.array_equal(image.get_color(), self.nparray_color))
        self.assertTrue(np.array_equal(image.get_grey(), self.nparray_grey))

    def test_init_grey(self):
        image = Image(self.nparray_grey)
        # test
        self.assertTrue(np.array_equal(image.get_color(), self.nparray_color))
        self.assertTrue(np.array_equal(image.get_grey(), self.nparray_grey))

    def test_init_nok(self):
        self.assertRaises(ValueError, Image, "some string")
        self.assertRaises(ValueError, Image, None)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
