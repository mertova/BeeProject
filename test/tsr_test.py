import unittest
from pathlib import Path

import cv2

from table.table import Table
from tsr import GridExtraction


class IdentificationTest(unittest.TestCase):

    def test_tsr_form1(self):
        # given ... change result path
        output_path = Path('./results/11/')
        output_path.mkdir(parents=True, exist_ok=True)

        form = Path("../data/LHI-final/form_contrasted_31_clean.png")
        """
        form = cv2.imread('../data/form1/31.png')
        form = cv2.erode(form, None, iterations=1)
        cv2.convertScaleAbs(form, form, 1.2, 6)
        cv2.imwrite((output_path / 'form_contrasted_31.png').as_posix(), form)
        """

        # when
        tsr = GridExtraction(form, output_path, 40, 20)
        grid = tsr.extract(True)
        form_img = cv2.imread(form.as_posix())
        form_img = grid.render(form_img, True, True)
        cv2.imwrite((output_path / "grid_ref.png").as_posix(), form_img)

        img_wrong = cv2.imread("C:/Users/lmert/PhD/BeeProject/BeeProject-dataset/SIFT_final_31_empty/1999/147.png")
        img_wrong = grid.render(img_wrong, True, True)
        cv2.imwrite((output_path / "grid_img_wrong.png").as_posix(), img_wrong)

        img_corr = cv2.imread("C:/Users/lmert/PhD/BeeProject/BeeProject-dataset/SIFT_final_31_empty/1999/146.png")
        img_corr = grid.render(img_corr, True, True)
        cv2.imwrite((output_path / "grid_img_corr.png").as_posix(), img_corr)


        # test
        self.assertEqual(type(grid), Table)
        self.assertEqual(grid.shape, (20, 15))
        print(grid)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
