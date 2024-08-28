import os
import unittest
from pathlib import Path

import cv2
import numpy as np

from image_processing.image import Image


class MyTestCase(unittest.TestCase):
    def setUp(self):
        current = os.getcwd()
        root_path = Path(current).parents[1]
        self.sample_path = (root_path /
                            "resources/play-data/test_data_2014/17_LHI_observation_reports_2014-1.png")
        if not self.sample_path.exists() or not self.sample_path.is_file():
            raise FileNotFoundError("No image, path " + self.sample_path.absolute().as_posix() + " is incorrect")

        self.nparray_color = cv2.imread(self.sample_path.as_posix())
        self.nparray_grey = cv2.cvtColor(self.nparray_color, cv2.COLOR_BGR2GRAY)
        self.out_path = root_path / "test/resources/results/test_image"

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
