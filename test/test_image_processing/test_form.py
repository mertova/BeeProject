import unittest

import cv2

from geometry.line import Line
from geometry.line_utils import render_lines
from image_processing.form import Form
from geometry.vertex import Vertex
from test.test_image_processing.test_image import TestImage


class TestReference(TestImage):

    def setUp(self):
        path_form = self.test_root_path / "./resources/form_contrasted_31_clean.png"
        if not path_form.is_file():
            raise FileNotFoundError("Form does not exist on the path " + path_form.absolute().as_posix())
        self.form_image = cv2.imread(path_form.absolute().as_posix())

    def test_init_and_dimensions(self):
        # dimensions 2481 x 3508
        form = Form(self.form_image)

        self.assertEqual(form.width, 2481)
        self.assertEqual(form.height, 3508)

        line_up = Line(Vertex(0, 0), Vertex(2481, 0))
        self.assertEqual(form.get_border_up(), line_up)
        line_down = Line(Vertex(0, 3508), Vertex(2481, 3508))
        self.assertEqual(form.get_border_down(), line_down)
        line_right = Line(Vertex(2481, 0), Vertex(2481, 3508))
        self.assertEqual(form.get_border_right(), line_right)
        line_left = Line(Vertex(0, 0), Vertex(0, 3508))
        self.assertEqual(form.get_border_left(), line_left)

    def test_hough_lines(self):
        form = Form(self.form_image)

        detected_lines = form.line_scanner_hough()

        canvas = self.form_image.copy()
        canvas = render_lines(canvas, detected_lines, (0, 140, 255))
        cv2.imwrite((self.out_path / "h_lines.png").as_posix(), canvas)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
