import unittest

from geometry.line import Line
from geometry.vertex import Vertex


class LineTest(unittest.TestCase):

    def _assertTupleAlmostEqual(self, tuple1, tuple2, places=7, msg=None):
        self.assertEqual(len(tuple1), len(tuple2))
        for a, b in zip(tuple1, tuple2):
            self.assertAlmostEqual(a, b, places=places, msg=msg)

    def test_intersects(self):
        # given
        a1 = Vertex(2, 1)
        b1 = Vertex(6, 5)
        line1 = Line(a1, b1)

        a2 = Vertex(3, 1)
        b2 = Vertex(4, 5)
        line2 = Line(a2, b2)

        # when
        intersection = line1.intersects(line2)

        # test
        result = Vertex(3.33, 2.33)
        print(intersection)
        self.assertIsNotNone(intersection)
        self._assertTupleAlmostEqual(intersection.as_tuple(), result.as_tuple(), 2,
                                     "Intersection is not correct")

    def test_intersects_vertical(self):
        # given
        a1 = Vertex(1, 1)
        b1 = Vertex(4, 3)
        line1 = Line(a1, b1)

        # vertical line
        a2 = Vertex(3, 0)
        b2 = Vertex(3, 5)
        line2 = Line(a2, b2)

        # when
        intersection = line1.intersects(line2)

        # test
        result = Vertex(3.0, 2.33)
        print(intersection)
        self.assertIsNotNone(intersection)
        self._assertTupleAlmostEqual(intersection.as_tuple(), result.as_tuple(), 2,
                                     "Intersection is not correct")

    def test_intersects_vertical_vertical(self):
        # given
        a1 = Vertex(2, 0)
        b1 = Vertex(2, 5)
        line1 = Line(a1, b1)

        a2 = Vertex(4, -1)
        b2 = Vertex(4, 3)
        line2 = Line(a2, b2)

        # when
        intersection = line1.intersects(line2)

        # test
        self.assertIsNone(intersection)

    def test_intersects_horizontal(self):
        # given
        a1 = Vertex(1, 1)
        b1 = Vertex(3, 5)
        line1 = Line(a1, b1)

        # horizontal line
        a2 = Vertex(0, 2)
        b2 = Vertex(5, 2)
        line2 = Line(a2, b2)

        # when
        intersection = line1.intersects(line2)

        # test
        result = Vertex(1.5, 2.0)
        print(intersection)
        self.assertIsNotNone(intersection)
        self._assertTupleAlmostEqual(intersection.as_tuple(), result.as_tuple(), 2,
                                     "Intersection is not correct")

    def test_intersects_horizontal_vertical(self):
        # given
        a1 = Vertex(-1, -1)
        b1 = Vertex(-1, 5)
        line1 = Line(a1, b1)

        a2 = Vertex(-3, 2)
        b2 = Vertex(5, 2)
        line2 = Line(a2, b2)

        # when
        intersection = line1.intersects(line2)

        # test
        result = Vertex(-1.0, 2.0)
        print(intersection)
        self.assertIsNotNone(intersection)
        self._assertTupleAlmostEqual(intersection.as_tuple(), result.as_tuple(), 2,
                                     "Intersection is not correct")

    def test_intersects_extends_line(self):
        # given
        a1 = Vertex(1, 1)
        b1 = Vertex(3, 3)
        line1 = Line(a1, b1)

        a2 = Vertex(4, 5)
        b2 = Vertex(5, 3)
        line2 = Line(a2, b2)

        # when
        intersection = line1.intersects(line2)

        # test
        result = Vertex(4.33, 4.33)
        print(intersection)
        self.assertIsNotNone(intersection)
        self._assertTupleAlmostEqual(intersection.as_tuple(), result.as_tuple(), 2,
                                     "Intersection is not correct")

    def test_intersects_outside(self):
        # given
        a1 = Vertex(1, 1)
        b1 = Vertex(2, 1)
        line1 = Line(a1, b1)

        a2 = Vertex(1, 5)
        b2 = Vertex(2, 4)
        line2 = Line(a2, b2)

        # when
        intersection = line1.intersects(line2)

        # test
        self.assertIsNone(intersection)

    def test_point_within(self):
        pass

    def test_line_set_intersections(self):
        # given
        a = Vertex(0, 5)
        b = Vertex(5, 5)
        line = Line(a, b)

        a1 = Vertex(1, 1)
        b1 = Vertex(3, 3)
        line1 = Line(a1, b1)

        a2 = Vertex(1, 5)
        b2 = Vertex(3, 5)
        line2 = Line(a2, b2)

        a3 = Vertex(-1, 4)
        b3 = Vertex(3, 4)
        line3 = Line(a3, b3)

        a4 = Vertex(-1, 7)
        b4 = Vertex(-3, 8)
        line4 = Line(a4, b4)

        # when
        list_lines = [line1, line2, line3, line4]
        intersections = line.line_set_intersections(list_lines, False)

        # test
        # (5.0, 5.0), None, None, (3.0, 5.0)
        results = (5.0, 3.0)
        print(intersections)
        self.assertIsNotNone(intersections)
        self._assertTupleAlmostEqual(intersections, results, 2, "Intersections are not correct")


if __name__ == '__main__':
    unittest.main()
    print('Done!')
