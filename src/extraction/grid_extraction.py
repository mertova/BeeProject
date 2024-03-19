from pathlib import Path

from extraction.grid import Grid
from extraction.grid_rendering import render_cells
from extraction.template import Template
from utils import line_utils, point_utils


class GridExtraction:
    def __init__(self, output_dir: Path, eps_h, eps_v, template: Template):
        self.out_dir = output_dir.absolute()
        self.debug_dir = self.out_dir / "debug_grid_recognition"
        self.eps_h = eps_h
        self.eps_v = eps_v
        self.template = template

    def extract(self, debug):
        if self.eps_h is None or self.eps_v is None:
            print("eps_h and eps_v are required")
            exit(1)

        if type(self.eps_h) is not int or type(self.eps_v) is not int:
            print("eps_h and eps_v must be convertable to integer")
            exit(1)

        print("Extracting grid ...")
        grid = self.process_pipeline()

        if debug:
            self.debug_dir.mkdir(parents=True, exist_ok=True)
            render_cells(grid, self.debug_dir, True)
        else:
            grid.export_json(self.debug_dir)
        return grid

    def process_pipeline(self) -> Grid:
        # line recognition with hough algorithm
        h_lines = line_utils.line_scanner_hough(self.template)

        # get ordered positions with all borderlines - clustered
        points = point_utils.find_border_points(self.template, h_lines, self.eps_h, self.eps_v)

        # find lines
        grid_lines_vertical = line_utils.grid_lines_from_points(points[0], points[1], False, self.template.width,
                                                                self.template.height)
        grid_lines_horizontal = line_utils.grid_lines_from_points(points[2], points[3], True, self.template.width,
                                                                  self.template.height)
        # todo
        grid_lines_horizontal.pop(1)

        # get dimensions
        shape = (len(grid_lines_vertical) - 1, len(grid_lines_horizontal) - 1)

        # intersections of all lines
        intersections = line_utils.line_sets_intersections(grid_lines_horizontal, grid_lines_vertical)

        # create bounding boxes of all cells
        cells = point_utils.boxes_form_points(intersections)

        return Grid(self.template, cells, shape)
