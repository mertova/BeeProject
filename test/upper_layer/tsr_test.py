import os
import unittest
from pathlib import Path

import cv2

from table.table import Table
from tsr import Tsr


class TsrTest(unittest.TestCase):

    output_path = None
    test_root_path = None

    @classmethod
    def setUpClass(cls):

        cls.test_root_path = Path(os.getcwd()).parents[0]

        cls.output_path = cls.test_root_path / "resources/results/test_tsr/"
        cls.output_path.mkdir(parents=True, exist_ok=True)
        cls.form1_path = Path("resources/form1.png")


    def test_tsr_form1(self):
        # given ... change result path

        form = Path("../../resources/LHI-final/form_contrasted_31_clean.png")
        """
        form = cv2.imread('../resources/form1/31.png')
        form = cv2.erode(form, None, iterations=1)
        cv2.convertScaleAbs(form, form, 1.2, 6)
        cv2.imwrite((output_path / 'form_contrasted_31.png').as_posix(), form)
        """

        # when
        tsr = Tsr(form, output_path, 40, 20)
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

    def print_stuff(self):
        if debug:
            canvas = self.form.get_color().copy()
            canvas = render_lines(canvas, grid_lines_horizontal, (0, 140, 255) )
            canvas = render_lines(canvas, grid_lines_vertical, (0, 140, 255) )
            cv2.imwrite((debug_dir / "grid_lines.png").as_posix(), canvas)
        """
        if debug:
            canvas = self.form.get_color().copy()
            for points in border_points:
                canvas = self._debug_render_points(canvas, points)
            cv2.imwrite("border_points.png", canvas)
        """

        if debug:
            canvas = self.form.get_color().copy()
            canvas = table.render(canvas, False, True)
            cv2.imwrite((debug_dir / "grid-text.png").as_posix(), canvas)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
