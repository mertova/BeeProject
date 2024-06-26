from pathlib import Path
import json

from src.table.cell import Cell


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
            output['cells'].append(cell.__dict__())
        with open(output_file, 'w') as f:
            json.dump(output, f, sort_keys=True, indent=4)

    def import_json(self, grid_json: dict):
        self.template_path = grid_json['template']
        self.shape = tuple(grid_json['shape'])
        cells = []
        for cell_json in grid_json['cells']:
            cell = Cell()
            cell.import_json(cell_json)
            cells.append(cell)
        self._cells = cells

    def render(self, include_canvas: bool, canvas=None):
        """
        Render the grid cells to the template
        :param canvas:
        :param include_canvas: if template image should be used as a background
        """
        if not include_canvas:
            canvas = (canvas.copy() * 0) + 255
        if self._cells is not None:
            for cell in self._cells:
                canvas = cell.render(canvas)
        return canvas

    def __str__(self):
        self._cells.sort()
        result = f"Grid( \n"
        col = 0
        for cell in self._cells:
            if col != cell.col_id:
                result += "\n"
                col = cell.col_id
            result += str(cell) + ', '
        return result
