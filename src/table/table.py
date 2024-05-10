from pathlib import Path

import json

from table.cell import Cell
from table.template import Template


class Table:
    def __init__(self, template: Template = None, cells: list[Cell] = None, shape: tuple = None):
        self.template = template
        self.cells = cells
        self.shape = shape

    def get_active_cells(self):
        return filter(lambda c: c.is_active, self.cells)

    def activate(self, indexes):
        self.cells.sort()
        for cell in self.cells:
            if cell.id in indexes:
                cell.activate_cell()

    def export_json(self, output_dir: Path):
        output_file = output_dir / "grid.json"
        output = {'template': self.template.path.as_posix(), 'shape': self.shape, 'cells': []}
        for cell in self.cells:
            output['cells'].append(cell.export_dict())
        with open(output_file, 'w') as f:
            json.dump(output, f, sort_keys=True, indent=4)

    def import_json(self, grid_json: dict):
        template_path = Path(grid_json['template'])
        self.template = Template(template_path)
        self.shape = tuple(grid_json['shape'])
        cells = []
        for cell_json in grid_json['cells']:
            cell = Cell()
            cell.import_json(cell_json)
            cells.append(cell)
        self.cells = cells

    def __str__(self):
        self.cells.sort()
        result = f"Grid( \n"
        row = 0
        for cell in self.cells:
            if row != cell.row_id:
                result += "\n"
                row = cell.row_id
            result += str(cell) + ' '
        return result
