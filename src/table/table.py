from pathlib import Path
import json
import cv2
from cell import Cell
from transformator.template import Template


class Table:
    def __init__(self, template_path: str = None, cells: list[Cell] = None, shape: tuple = None):
        self.template_path = template_path
        self._cells = cells
        self.shape = shape

    def get_cells(self):
        return self._cells

    def get_active_cells(self):
        return filter(lambda c: c.is_active, self._cells)

    def activate(self, indexes):
        self._cells.sort()
        for cell in self._cells:
            if cell.id in indexes:
                cell.activate_cell()

    def export_json(self, output_dir: Path):
        output_file = output_dir / "grid.json"
        output = {'template': self.template_path, 'shape': self.shape, 'cells': []}
        for cell in self._cells:
            output['cells'].append(cell.export_dict())
        with open(output_file, 'w') as f:
            json.dump(output, f, sort_keys=True, indent=4)

    def import_json(self, grid_json: dict):
        self.template_path = Template(grid_json['template'])
        self.shape = tuple(grid_json['shape'])
        cells = []
        for cell_json in grid_json['cells']:
            cell = Cell()
            cell.import_json(cell_json)
            cells.append(cell)
        self._cells = cells

    def render(self, include_canvas: bool = False):
        """
        TODO
        Render the grid cells to the template
        :param include_canvas: if template image should be used as a background
        """
        canvas = self.get_canvas(include_canvas)
        rec_color = (0, 255, 60)
        text_color = (200, 0, 60)
        if self.cells is not None:
            for cell in self.cells:
                pt1 = cell.pt1
                pt2 = cell.pt2
                canvas = cv2.rectangle(canvas, pt1, pt2, rec_color, 2)
                canvas = cv2.putText(canvas, str(cell), pt1,
                                     cv2.FONT_HERSHEY_SIMPLEX, 1, text_color,
                                     2, cv2.LINE_AA, False)
        return canvas

    def get_canvas(self, include_canvas: bool = False):
        img = cv2.imread(self.template_path)
        if include_canvas:
            return img.copy()
        return (img.copy() * 0) + 255

    def __str__(self):
        self._cells.sort()
        result = f"Grid( \n"
        row = 0
        for cell in self._cells:
            if row != cell.row_id:
                result += "\n"
                row = cell.row_id
            result += str(cell) + ' '
        return result
