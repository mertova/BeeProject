from pathlib import Path

import cv2
from shapely import LineString

from cell import Cell
from image import Image
import json


class Grid:
    def __init__(self, template: Image, cells: list[Cell], intersections, lines_h, lines_v):
        self.template = template
        self.cells = cells
        self.intersections = intersections
        self.lines_h = lines_h
        self.lines_v = lines_v
        self.dimensions = (len(self.lines_v) - 1, len(self.lines_h) - 1)

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

    def render_boxes(self, output_dir: Path, include_canvas: bool = False):
        if include_canvas:
            canvas = self.template.image_color.copy()
        else:
            canvas = (self.template.image_color.copy() * 0) + 255

        line_extraction_dir = output_dir / "line_extraction"
        line_extraction_dir.mkdir(exist_ok=True)

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
        cv2.imwrite((line_extraction_dir / "boxes.png").as_posix(), canvas)

    def render_lines(self, output_dir: Path, include_canvas: bool = False):
        if include_canvas:
            canvas = self.template.image_color.copy()
        else:
            canvas = (self.template.image_color.copy() * 0) + 255

        line_extraction_dir = output_dir / "line_extraction"
        line_extraction_dir.mkdir(exist_ok=True)
        color_horizontal = (200, 0, 60)
        color_vertical = (0, 255, 60)
        color_points = (0, 0, 180)
        canvas = write_lines(canvas, self.lines_v, color_vertical)
        canvas = write_lines(canvas, self.lines_h, color_horizontal)
        for line_intersections in self.intersections:
            canvas = write_points(canvas, line_intersections, color_points)
        # Save the result image - detected lines and intersections
        cv2.imwrite((line_extraction_dir / "lines.png").as_posix(), canvas)

    def export_json(self, output_file):
        output = {'cells': []}
        for cell in self.cells:
            output['cells'].append(cell.as_dict())
        with open(output_file, 'w') as f:
            json.dump(output, f, sort_keys=True, indent=4)


def write_points(image, points: list[tuple], color: tuple):
    for point in points:
        if point is not None:
            cv2.circle(image, (point[0], point[1]), radius=5, color=color, thickness=-1)
    return image


def write_lines(image, lines: list, color):
    """
    write lines to the image
    """
    if lines is None:
        return image
    for line in lines:
        if type(line) is tuple:
            pt1, pt2 = line
            cv2.line(image, pt1, pt2, color, 4)
        elif type(line) is LineString:
            pt1 = (int(line.xy[0][0]), int(line.xy[1][0]))
            pt2 = (int(line.xy[0][1]), int(line.xy[1][1]))
            cv2.line(image, pt1, pt2, color, 4)
    return image
