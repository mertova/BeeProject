import json
import unittest
from pathlib import Path

import cv2
import numpy as np

from geometry.vertex import Vertex
from table.cell import Cell
from table.table import Table


class TableTest(unittest.TestCase):
    blank_canvas = np.zeros((300, 500, 3), np.uint8)

    # cell left up
    pt1_cell1 = Vertex(20, 50)
    pt2_cell1 = Vertex(60, 80)
    cell1 = Cell(5, 3, pt1_cell1, pt2_cell1)
    # cell right up
    pt1_cell2 = Vertex(62, 50)
    pt2_cell2 = Vertex(103, 82)
    cell2 = Cell(5, 4, pt1_cell2, pt2_cell2)
    # cell left down
    pt1_cell3 = Vertex(21, 82)
    pt2_cell3 = Vertex(60, 115)
    cell3 = Cell(6, 3, pt1_cell3, pt2_cell3)
    # cell right down
    pt1_cell4 = Vertex(62, 81)
    pt2_cell4 = Vertex(105, 113)
    cell4 = Cell(6, 4, pt1_cell4, pt2_cell4)

    table = Table(None, [cell1, cell2, cell3, cell4], (2, 2))

    def test_export_cell_json(self):
        # given
        pt1 = Vertex(20, 50)
        pt2 = Vertex(30, 60)
        given_cell = Cell(5, 3, pt1, pt2)

        # when
        actual_json = given_cell.__dict__()

        # then
        cell_id = 'D5'
        expected_json = {'text': cell_id, 'pt1': pt1.__dict__(), 'pt2': pt2.__dict__()}
        self.assertEqual(actual_json, expected_json)
        print(actual_json)

    def test_export_table_json(self):
        cells = [self.cell1.__dict__(), self.cell2.__dict__(), self.cell3.__dict__(), self.cell4.__dict__()]
        expected_json = {'template': None, 'cells': cells, 'shape': tuple(self.table.shape)}
        # when
        self.table.export_json(Path("./"))
        # then
        with open(Path("./table.json"), "r") as f:
            actual_json = json.load(f)
        actual_json['shape'] = tuple(self.table.shape)
        self.assertEqual(expected_json, actual_json)

    def test_activate_table_cells(self):
        # given
        indexes = ['D5', 'E6']

        # when
        self.table.activate(indexes)

        # then
        for cell in self.table.get_cells():
            if cell.text == 'D5' or cell.text == 'E6':
                self.assertTrue(cell.is_active)
            else:
                self.assertFalse(cell.is_active)

    def test_import_table_json(self):
        new_table = Table()
        try:
            with open(Path("./table.json"), "r") as f:
                new_table.import_json(json.load(f))
        except FileNotFoundError:
            print("File to import not found: table.json")

        self.assertEqual(self.table, new_table)

    def test_render_table(self):
        img = self.table.render(self.blank_canvas, False, True)
        cv2.imshow('table', img)
        cv2.waitKey(0)

        self.assertEqual(img.shape, (300, 500, 3))


if __name__ == '__main__':
    unittest.main()
    print("DONE")
