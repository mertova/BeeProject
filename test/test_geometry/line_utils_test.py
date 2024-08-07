import unittest

import cv2
import numpy as np

from geometry import line_utils
from geometry.line import Line
from geometry.vertex import Vertex


class LineUtilsTest(unittest.TestCase):

    def test_create_lines_from_points(self):
        # given
        pt_set1 = [10, 55, 82, 320]
        pt_set2 = [12, 60, 80, 315]

        # when
        lines = line_utils.create_lines_from_points(pt_set1, pt_set2, False, 500)

        # test
        line1 = Line(Vertex(0, 10), Vertex(500, 12))
        line2 = Line(Vertex(0, 55), Vertex(500, 60))
        line3 = Line(Vertex(0, 82), Vertex(500, 80))
        line4 = Line(Vertex(0, 320), Vertex(500, 315))
        result = [line1, line2, line3, line4]
        self.assertEqual(set(lines), set(result))

        print(lines)
        canvas = np.zeros((500, 1000)) + 255
        cv2.imshow("clean canvas", canvas)
        line_canvas = line_utils.render_lines(canvas, lines, (0,0,0 ))
        cv2.imshow("horizontal lines", line_canvas)
        cv2.waitKey(0)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
