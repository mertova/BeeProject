from pathlib import Path

import cv2

from geometry.vertex import Vertex
from geometry.line_utils import create_lines_from_points, render_lines
from table.table import Table
from geometry.line import Line
from geometry.utils import cluster
from image_processing.form import Form
from geometry import line_utils
from table.cell import Cell


def cells_form_vertices(p: [[Vertex]]):
    if p is None or len(p) == 0:
        return None

    cells = []
    for i in range(len(p) - 1):
        sorted_points1 = sorted(p[i], key=lambda x: (x[0], x[1]))
        sorted_points2 = sorted(p[i + 1], key=lambda x: (x[0], x[1]))
        if len(sorted_points1) != len(sorted_points2):
            raise ValueError('Bounding boxes must have the same number of points')
        for j in range(len(sorted_points1) - 1):
            p1 = Vertex(sorted_points1[j][0], sorted_points1[j][1])
            p2 = Vertex(sorted_points2[j + 1][0], sorted_points2[j + 1][1])
            cell = Cell(i, j, p1, p2)
            cells.append(cell)
    return cells


def make_grid_lines(points1: list, points2: list, vertical: bool, width: int, height: int) -> list[Line]:
    """Makes a grid lines given two sets of numbers. Problem when those 2 sets are not equal in length.
    """
    if points1 is None or points2 is None or len(points1) != len(points2):
        return []
    if vertical:
        sorted_lines = create_lines_from_points(points1, points2, vertical, height)
    else:
        sorted_lines = create_lines_from_points(points1, points2, vertical, width)
    return sorted_lines


class GridExtraction:
    form_path: Path
    out_dir: Path
    eps_h: int
    eps_v: int
    form: Form

    def __init__(self, form_path: Path, output_dir: Path, eps_h: int, eps_v: int):
        self.out_dir = output_dir.absolute()
        self.eps_h = eps_h
        self.eps_v = eps_v
        self.form_path = form_path

    def extract(self, debug):
        if self.eps_h is None or self.eps_v is None or self.form_path is None or self.out_dir is None:
            print("Some of the attributes is None")
            exit(1)

        if type(self.eps_h) is not int or type(self.eps_v) is not int:
            print("eps_h and eps_v must be integer")
            exit(1)

        try:
            self.form = Form(cv2.imread(self.form_path.as_posix()))
        except Exception as e:
            print("loading of the form failed")
            exit(1)

        print("Extracting grid ...")
        grid = self._process_pipeline(debug)
        grid.export_json(self.out_dir)
        return grid

    def _process_pipeline(self, debug) -> Table:
        """
        Extract Table from the Form.
        :param debug: in case we want to render some steps of the process
        :return:
        """

        # line recognition with hough algorithm
        h_lines = self.form.line_scanner_hough()

        if debug:
            # todo
            debug_dir = self.out_dir / "table_extraction"
            debug_dir.mkdir(parents=True, exist_ok=True)

            canvas = self.form.get_color().copy()
            canvas = render_lines(canvas, h_lines, (0, 140, 255))
            cv2.imwrite((debug_dir / "h_lines.png").as_posix(), canvas)

        # get ordered positions with all borderlines - clustered
        border_points = self._find_border_points(h_lines)

        """
        if debug:
            canvas = self.form.get_color().copy()
            for points in border_points:
                canvas = self._debug_render_points(canvas, points)
            cv2.imwrite("border_points.png", canvas)
        """
        # find lines
        grid_lines_vertical = make_grid_lines(border_points[0], border_points[1], True, self.form.width,
                                              self.form.height)
        grid_lines_horizontal = make_grid_lines(border_points[2], border_points[3], False,
                                                self.form.width, self.form.height)

        if debug:
            canvas = self.form.get_color().copy()
            canvas = render_lines(canvas, grid_lines_horizontal, (0, 140, 255) )
            canvas = render_lines(canvas, grid_lines_vertical, (0, 140, 255) )
            cv2.imwrite((debug_dir / "grid_lines.png").as_posix(), canvas)

        # get dimensions
        shape = (len(grid_lines_vertical) - 1, len(grid_lines_horizontal) - 1)

        # intersections of all lines
        intersections = line_utils.set_to_set_intersections(grid_lines_horizontal, grid_lines_vertical)

        # create bounding boxes of all cells
        cells = cells_form_vertices(intersections)

        table = Table(self.form_path.as_posix(), cells, shape)

        if debug:
            canvas = self.form.get_color().copy()
            canvas = table.render(canvas, False, True)
            cv2.imwrite((debug_dir / "grid-text.png").as_posix(), canvas)

        return table

    def _find_border_points(self, h_lines: list[Line]) -> list[list[int]] | None:
        """
        Find border points for a result from the Hugh line segments.
        :param h_lines:
        :return: list of border points for each border in a sequence: [up, down, left, right]
        """
        if h_lines is None or len(h_lines) == 0:
            print("No hough lines found")
            return None

        # up, down, left, right
        clustered_points = [self._get_optimal_line_points(h_lines, self.form.get_border_up(), self.form.width,
                                                          False),
                            self._get_optimal_line_points(h_lines, self.form.get_border_down(), self.form.width,
                                                          False),
                            self._get_optimal_line_points(h_lines, self.form.get_border_left(), self.form.height,
                                                          True),
                            self._get_optimal_line_points(h_lines, self.form.get_border_right(), self.form.height,
                                                          True)]
        return clustered_points

    def _get_optimal_line_points(self, h_lines: list[Line], line: Line, size: int, vertical: bool) -> list[int]:
        border_points_simpl = line.line_set_intersections(h_lines, vertical)
        if vertical:
            optimal_points = cluster(border_points_simpl, self.eps_v)
        else:
            optimal_points = cluster(border_points_simpl, self.eps_h)
        optimal_points.append(size)
        optimal_points.append(0)
        return sorted(optimal_points)


    def _debug_render_points(self, canvas, points):
        for point in points:
            canvas = cv2.circle(canvas, point.asTuple(), 2,  (0, 140, 255))
        return canvas
