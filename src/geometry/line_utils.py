from geometry.line import Line
from geometry.vertex import Vertex


def set_to_set_intersections(horizontal: list[Line], vertical: list[Line]) -> list[list[(int, int)]]:
    if vertical is None or horizontal is None:
        return []
    result_points = []
    horizontal_points = []
    for h in horizontal:
        for v in vertical:
            int_pt = h.intersects(v)
            if type(int_pt) is Vertex:
                horizontal_points.append((int(int_pt.x), int(int_pt.y)))
        result_points.append(horizontal_points)
        horizontal_points = []
    return result_points


def create_lines_from_points(position_set1: list[int], position_set2: list[int], vertical: bool,
                             max_val: int) -> list[Line]:
    if len(position_set1) != len(position_set2):
        raise ValueError('points are not matching')
    optimal_lines = []
    for i in range(len(position_set1)):
        if vertical:
            optimal_lines.append(Line(Vertex(int(position_set1[i]), 0), Vertex(int(position_set2[i]), max_val)))
        else:
            optimal_lines.append(Line(Vertex(0, int(position_set1[i])), Vertex(max_val, int(position_set2[i]))))
    return optimal_lines


def render_lines(canvas, lines: list[Line], color):
    """
    write lines to the image
    """
    result_img = canvas.copy()
    if lines is None:
        return result_img
    for line in lines:
        result_img = line.render(result_img, color)
    return result_img
