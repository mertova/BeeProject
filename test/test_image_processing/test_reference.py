import os
import unittest
from pathlib import Path

import cv2
import numpy as np

from image_processing.reference import Reference
from test.test_image_processing.test_image import TestImage


class TestReference(TestImage):
    current = os.getcwd()
    root_path = Path(current).parents[0]
    out_path = root_path / "test/resources/results/image_processing"
    out_path.mkdir(exist_ok=True, parents=True)

    reference_path = root_path / "resources/reference.png"
    if not reference_path.is_file():
        raise FileNotFoundError("No image, path " + reference_path.absolute().as_posix() + " is incorrect")

    reference_image = cv2.imread(reference_path.as_posix())
    sift_reference = Reference(reference_image, "sift")
    orb_reference = Reference(reference_image, "orb")

    def test_pen_elimination(self):
        self.sift_reference.pen_elimination()
        cv2.imshow("pen eliminated", self.sift_reference.get_color())
        cv2.waitKey(0)

    def test_transformation_sift(self):
        other_image = cv2.imread((self.root_path / "resources/scans/1.png").as_posix())
        if other_image is None:
            raise FileNotFoundError("No image, path " + self.root_path.as_posix() +
                                    "/ resources/scans/1.png is incorrect")

        aligned = self.sift_reference.map_img_to_ref(other_image)

        # test
        self.assertTrue(np.array_equal(aligned.shape, self.reference_image.shape))

    def test_transformation_orb(self):
        other_image = cv2.imread((self.root_path / "resources/scans/2.png").as_posix())
        if other_image is None:
            raise FileNotFoundError("No image, path " + self.root_path.as_posix() +
                                    "/ resources/scans/2.png is incorrect")

        aligned = self.orb_reference.map_img_to_ref(other_image)

        # test
        self.assertTrue(np.array_equal(aligned.shape, self.reference_image.shape))


if __name__ == '__main__':
    unittest.main()
    print('Done!')
