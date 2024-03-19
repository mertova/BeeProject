from pathlib import Path

import cv2
from shapely import LineString


def render_cells(grid, output_dir: Path, include_canvas: bool = False):
    canvas = get_canvas(grid.template.template_img, include_canvas)

    rec_color = (0, 255, 60)
    text_color = (200, 0, 60)
    if grid.cells is not None:
        for cell in grid.cells:
            pt1 = cell.pt1
            pt2 = cell.pt2
            canvas = cv2.rectangle(canvas, pt1, pt2, rec_color, 2)
            canvas = cv2.putText(canvas, str(cell), pt1,
                                 cv2.FONT_HERSHEY_SIMPLEX, 1, text_color,
                                 2, cv2.LINE_AA, False)
    cv2.imwrite((output_dir / "boxes.png").as_posix(), canvas)


def render_lines(grid, output_dir: Path, lines_h, lines_v, intersections, include_canvas: bool = False):
    canvas = get_canvas(grid.template.image_color, include_canvas)

    color_horizontal = (200, 0, 60)
    color_vertical = (0, 255, 60)
    color_points = (0, 0, 180)
    canvas = write_lines(canvas, lines_v, color_vertical)
    canvas = write_lines(canvas, lines_h, color_horizontal)
    for line_intersections in intersections:
        canvas = write_points(canvas, line_intersections, color_points)
    # Save the result image - detected lines and intersections
    cv2.imwrite((output_dir / "lines.png").as_posix(), canvas)


def get_canvas(img, include_canvas: bool = False):
    if include_canvas:
        return img.copy()
    return (img.copy() * 0) + 255


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
