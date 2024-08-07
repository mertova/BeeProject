import unittest

from geometry.vertex import Vertex

from table.annotations import OcrAnnotation, CellAnnotation
from table.cell import Cell


class AnnotationsTest(unittest.TestCase):

    def test_init_ocr_annotation(self):
        # given
        pt1 = Vertex(0, 0)
        pt2 = Vertex(30, 40)
        confidence = 0.9
        text = "Hello World"

        # when
        annotation = OcrAnnotation(pt1, pt2, text, confidence)

        # then
        self.assertIsNotNone(annotation)
        self.assertEqual(type(annotation), OcrAnnotation)
        self.assertEqual(annotation.text, text)
        self.assertEqual(annotation.confidence, confidence)
        self.assertEqual(annotation.pt1, pt1)
        self.assertEqual(annotation.pt2, pt2)

        print(annotation)

    def test_init_cell_annotation(self):
        pt1 = Vertex(0, 0)
        pt2 = Vertex(30, 40)
        cell = Cell(2, 3, pt1, pt2)

        annotation = CellAnnotation(cell)

        self.assertIsNotNone(annotation)
        self.assertEqual(type(annotation), CellAnnotation)
        self.assertEqual(annotation.cell, cell)

    def test_concatenate_text_confidence(self):
        pt1 = Vertex(0, 0)
        pt2 = Vertex(30, 40)
        cell = Cell(2, 3, pt1, pt2)
        annotation = CellAnnotation(cell)

        self.assertIsNotNone(annotation, "Initiation of cell annotation failed")
        self.assertEqual(type(annotation), CellAnnotation, "Initiation of cell annotation failed")

        conf1 = 0.7
        conf2 = 0.8
        conf3 = 0.9
        text1 = "Hello"
        text2 = " "
        text3 = "World"
        annotation.concatenate_text_confidence(text1, conf1)
        annotation.concatenate_text_confidence(text2, conf2)
        annotation.concatenate_text_confidence(text3, conf3)

        self.assertEqual(annotation.text, "Hello World")
        # todo confidence is 8.25
        self.assertEqual(annotation.confidence, 0.8)

    def test_concatenate_text_confidence_None(self):
        pass

    def test_add_snippet(self):
        pass

    def test_compose_cell_annotations(self):
        pass

    def test_sort_ocr_annotations(self):
        pass


if __name__ == '__main__':
    unittest.main()
    print('Done')
