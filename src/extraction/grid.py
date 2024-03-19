from pathlib import Path

import json

from extraction.cell import Cell
from extraction.template import Template


class Grid:
    def __init__(self, template: Template = None, cells: list[Cell] = None, shape: tuple = None):
        self.template = template
        self.cells = cells
        self.shape = shape

    def export_json(self, output_dir: Path):
        output_file = output_dir / "grid.json"
        output = {'template': self.template.path.as_posix(), 'cells': []}
        for cell in self.cells:
            output['cells'].append(cell.as_dict())
        with open(output_file, 'w') as f:
            json.dump(output, f, sort_keys=True, indent=4)

    def import_json(self, file_path: Path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        template_path = Path(data['template'])
        template = Template(template_path)
        self.template = template

        cells = []
        for cell in data['cells']:
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
