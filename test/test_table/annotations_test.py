import json
import unittest
from pathlib import Path

from geometry.vertex import Vertex
from table import annotations

from table.annotations import OcrAnnotation, CellAnnotation
from table.cell import Cell
from table.table import Table

REPO_ROOT = Path(__file__).resolve().parents[2]
TABLE_JSON = REPO_ROOT / "test" / "resources" / "form1" / "form1_table_31.json"


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

    def _load_table(self):
        with open(TABLE_JSON, 'r') as data:
            table = Table()
            table.import_json(json.load(data))
        table.activate(['H3', 'I3', 'I4'])
        return table

    def test_compose_cell_annotations(self):
        table = self._load_table()
        # a couple of synthetic OCR hits landing inside cell H3, matching its pt1/pt2 bounds
        h3 = next(c for c in table.get_cells() if c.text == 'H3')
        mid_x = (h3.pt1.x + h3.pt2.x) // 2
        mid_y = (h3.pt1.y + h3.pt2.y) // 2
        ocr_annotations = [
            OcrAnnotation(Vertex(mid_x - 5, mid_y - 5), Vertex(mid_x, mid_y), "12", 0.9),
            OcrAnnotation(Vertex(mid_x, mid_y), Vertex(mid_x + 5, mid_y + 5), ".4", 0.85),
        ]
        sorted_ocr_annotations = annotations.sort_ocr_annotations(ocr_annotations, table)

        # test
        for c, a in sorted_ocr_annotations.items():
            result = annotations.compose_cell_annotations(c, a, 0.75)
            self.assertEqual(type(result), CellAnnotation)

    def test_sort_ocr_annotations(self):
        table = self._load_table()
        h3 = next(c for c in table.get_cells() if c.text == 'H3')
        mid_x = (h3.pt1.x + h3.pt2.x) // 2
        mid_y = (h3.pt1.y + h3.pt2.y) // 2
        ocr_annotations = [OcrAnnotation(Vertex(mid_x - 2, mid_y - 2), Vertex(mid_x, mid_y), "12", 0.9)]

        # test
        result = annotations.sort_ocr_annotations(ocr_annotations, table)
        self.assertIn('H3', result)
        self.assertEqual(len(result['H3']), 1)


if __name__ == '__main__':
    unittest.main()
    print('Done')
