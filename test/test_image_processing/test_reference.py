import unittest
from pathlib import Path

import cv2
import numpy as np

from image_processing.reference import Reference
from test.test_image_processing.test_image import TestImage


class TestReference(TestImage):
    def setUp(self):
        reference_path = self.test_root_path / "resources/form1_reference.png"
        if not reference_path.is_file():
            raise FileNotFoundError("No image, path " + reference_path.absolute().as_posix() + " is incorrect")

        self.sample_data = Path(self.test_root_path).joinpath("resources/scans/")
        if not self.sample_data.exists():
            raise NotADirectoryError("No path, " + self.sample_data.absolute().as_posix() + " is incorrect")

        self.reference_image = cv2.imread(reference_path.as_posix())
        self.sift_reference = Reference(self.reference_image, "sift")
        self.orb_reference = Reference(self.reference_image, "orb")

    def test_pen_elimination(self):
        # run
        self.sift_reference.pen_elimination()
        # visualise
        cv2.imshow("pen eliminated", self.sift_reference.get_color())
        cv2.waitKey(0)

    def test_transformation_sift(self):
        # set
        other_image = cv2.imread((self.test_root_path / "resources/scans/1.png").as_posix())
        if other_image is None:
            raise FileNotFoundError("No image, path " + self.test_root_path.as_posix() +
                                    "/ resources/scans/1.png is incorrect")
        # run
        aligned = self.sift_reference.map_img_to_ref(other_image)

        # test
        self.assertTrue(np.array_equal(aligned.shape, self.reference_image.shape))

    def test_transformation_orb(self):
        # set
        other_image = cv2.imread((self.test_root_path / "resources/scans/2.png").as_posix())
        if other_image is None:
            raise FileNotFoundError("No image, path " + self.test_root_path.as_posix() +
                                    "/ resources/scans/2.png is incorrect")
        # run
        aligned = self.orb_reference.map_img_to_ref(other_image)
        # test
        self.assertTrue(np.array_equal(aligned.shape, self.reference_image.shape))

    def test_add_weighted(self):
        p = self.sample_data.glob('*.png')
        i = 0
        for x in p:
            if i > 2:
                break
            print("transforming image " + x.as_posix())
            img = cv2.imread(x.as_posix(), cv2.IMREAD_GRAYSCALE)
            img = self.sift_reference.map_img_to_ref(img)
            self.sift_reference.add_weighted(img)
            i += 1
        cv2.imshow("pen eliminated", self.sift_reference.get_color())
        cv2.waitKey(0)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
