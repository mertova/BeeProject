import unittest

import cv2
import numpy as np

from geometry.rectangle import Rectangle
from geometry.vertex import Vertex


def show_rectangle_and_point(rectangle: Rectangle, point: Vertex, caption: str):
    blank_canvas = np.zeros((300, 300, 3), np.uint8)
    img = rectangle.render(blank_canvas)
    img = point.render(img, (0, 0, 200), 2)
    cv2.imshow(caption, img)
    cv2.waitKey(0)


class RectangleTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_constructor(self):
        # given
        pt1 = Vertex(0, 0)
        pt2 = Vertex(10, 10)
        text = "hi"

        # when
        rectangle = Rectangle(pt1, pt2, text)

        # test
        self.assertEqual(type(rectangle), Rectangle)
        self.assertEqual(rectangle.pt1, pt1)
        self.assertEqual(rectangle.pt2, pt2)
        self.assertEqual(rectangle.text, text)
        print(rectangle)

    def test_calculate_center(self):
        # given
        pt1 = Vertex(50, 10)
        pt2 = Vertex(80, 30)
        text = "hi"
        rectangle = Rectangle(pt1, pt2, text)

        # when
        rectangle.calculate_center()
        actual_center = rectangle.center

        # test
        expected_center = Vertex(65, 20)
        show_rectangle_and_point(rectangle, actual_center, "center")
        self.assertEqual(actual_center, expected_center)

        print("actual center: ", actual_center, "\nexpected center: ", expected_center)

    def test_contains_point(self):
        # given
        pt1 = Vertex(20, 20)
        pt2 = Vertex(150, 200)
        text = "hi"
        rectangle = Rectangle(pt1, pt2, text)

        # when
        point_inside = Vertex(50, 50)
        contains = rectangle.contains_point(point_inside)

        # test
        show_rectangle_and_point(rectangle, point_inside,  "contain")
        self.assertTrue(contains)
        print("actual center: ", point_inside)

    def test_does_not_contain_point(self):
        # given
        pt1 = Vertex(20, 20)
        pt2 = Vertex(150, 200)
        text = "hi"
        rectangle = Rectangle(pt2, pt1, text)

        # when
        point_outside = Vertex(10, 5)
        contains = rectangle.contains_point(point_outside)

        # test
        show_rectangle_and_point(rectangle, point_outside, "do not contain")
        self.assertFalse(contains)
        print("actual center: ", point_outside)

    def test_crop_image(self):
        # given
        pt1 = Vertex(20, 20)
        pt2 = Vertex(150, 200)
        text = "hi"
        rectangle = Rectangle(pt2, pt1, text)

        blank_canvas = np.zeros((300, 200, 3), np.uint8)
        cv2.rectangle(blank_canvas, pt1.as_tuple(), pt2.as_tuple(), (0, 0, 255), -1)

        blank_canvas_copy = blank_canvas.copy()
        pt1.render(blank_canvas_copy, (255, 0, 0), 2)
        pt2.render(blank_canvas_copy, (255, 0, 0), 2)
        cv2.imshow("rectangle", blank_canvas_copy)

        # test
        cropped_image = rectangle.crop_image(blank_canvas)
        cv2.imshow("cropped_rectangle", cropped_image)
        cv2.waitKey(0)
        print(cropped_image.shape)
        self.assertEqual((180, 130, 3), cropped_image.shape)

        for i in range(len(cropped_image)):
            for j in range(len(cropped_image[i])):
                x = cropped_image[i][j][0]
                y = cropped_image[i][j][1]
                z = cropped_image[i][j][2]
                self.assertTupleEqual((x, y, z), (0, 0, 255))


if __name__ == '__main__':
    unittest.main()
    print('Done!')
