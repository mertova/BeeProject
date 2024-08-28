import unittest

from geometry.vertex import Vertex


class VertexTest(unittest.TestCase):
    # todo: 1. type check 2. more than

    def test_init(self):
        vertex = Vertex(1, 3)
        self.assertEqual(vertex.x, 1)
        self.assertEqual(vertex.y, 3)

    def test_negative_number_init(self):
        self.assertRaises(ValueError, Vertex, -1, 3)

    def test_incorrect_type_number_init(self):
        # todo
        vertex = Vertex("1", 4.6)
        self.assertRaises(ValueError, Vertex, "1", 4.6)

    def test_is_more_than_1(self):
        # todo
        v1 = Vertex(1, 3)
        v2 = Vertex(2, 3)
        self.assertTrue(v2.is_more_than(v1))

    def test_is_more_than_2(self):
        v1 = Vertex(2, 4)
        v2 = Vertex(2, 3)
        self.assertTrue(v2.is_more_than(v1))

    def test_as_tuple(self):
        vertex = Vertex(2, 7)
        expected_tuple = vertex.as_tuple()
        actual_tuple = (2, 7)
        self.assertEqual(expected_tuple, actual_tuple)

    def test_dist(self):
        vertex = Vertex(2, 7)
        vertex_json = vertex.__dict__()
        expected_dict = {'x': 2, 'y': 7}
        self.assertEqual(expected_dict, vertex_json)

    def test_eq(self):
        v1 = Vertex(3, 5)
        v2 = Vertex(3, 5)
        self.assertTrue(v1 == v2)

    def test_not_eq(self):
        v1 = Vertex(3, 5)
        v2 = Vertex(3, 7)
        self.assertFalse(v1 == v2)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
