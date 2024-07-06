from pathlib import Path
import json

import numpy

from src.table.cell import Cell


class Table:
    """
    A class to represent a table in the given form.
    """

    template_path: str
    _cells: list[Cell]
    shape: (int, int)

    def __init__(self, template_path: str = None, cells: list[Cell] = None, shape: (int, int) = None):
        self.template_path = template_path
        self._cells = cells
        self.shape = shape

    def get_cells(self):
        return self._cells

    def get_active_cells(self):
        return filter(lambda c: c.is_active, self._cells)

    def activate(self, indexes):
        """
        activates all cells in the table with the given indexes
        :param indexes: cells to activate
        """
        for cell in self._cells:
            if cell.text in indexes:
                cell.activate_cell()

    def export_json(self, output_dir: Path):
        """
        Exports the table as a JSON file.
        :param output_dir: output directory.
        """
        output_file = output_dir / "table.json"
        output = {'template': self.template_path, 'shape': self.shape, 'cells': []}
        for cell in self._cells:
            output['cells'].append(cell.__dict__())
        with open(output_file, 'w') as f:
            json.dump(output, f, sort_keys=True, indent=4)

    def import_json(self, table_json: dict):
        """
        Import json file into a table
        :param table_json: json file to import
        """
        self.template_path = table_json['template']
        self.shape = tuple(table_json['shape'])
        cells = []
        for cell_json in table_json['cells']:
            cell = Cell()
            cell.import_json(cell_json)
            cells.append(cell)
        self._cells = cells

    def render(self, canvas: numpy.array, include_canvas: bool = False, include_text: bool = False) -> numpy.array:
        """
        Render the grid cells to the template
        :param canvas: canvas on which we render the grid cells
        :param include_canvas: if image should be used as a background or white background
        :param include_text: if text cells are included
        :return: rendered grid cells as image (numpy array)
        """
        if not include_canvas:
            canvas = (canvas.copy() * 0) + 255
        if self._cells is not None:
            for cell in self._cells:
                canvas = cell.render(canvas, include_text)
        return canvas

    def __str__(self):
        self._cells.sort()
        result = f"Table( \n"
        col = 0
        for cell in self._cells:
            if col != cell.col_id:
                result += "\n"
                col = cell.col_id
            result += str(cell) + ', '
        return result

    def __eq__(self, other):
        if isinstance(other, Table):
            return self._cells == other._cells
        return False

    def __hash__(self):
        return hash(self._cells)
