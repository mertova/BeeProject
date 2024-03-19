import cv2
import numpy as np
from shapely.geometry import LineString, Point

from extraction.template import Template


# x,y coordinates of the intersection of two input lines
# false if no intersection (determinant == 0)
def borders_intersections(border: LineString, l_set: list[LineString], vertical):
    if border is None or l_set is None:
        return []
    results = []
    for v in l_set:
        int_pt = line_intersection(border.coords, v.coords)
        if type(int_pt) is tuple:
            point = Point(int_pt[0], int_pt[1])
            if point.within(border):
                if vertical:
                    results.append(int_pt[1])
                else:
                    results.append(int_pt[0])
    return results


def line_sets_intersections(horizontal: list[LineString], vertical: list[LineString]) -> list[list[(int, int)]]:
    if vertical is None or horizontal is None:
        return []
    result_points = []
    horizontal_points = []
    for h in horizontal:
        for v in vertical:
            int_pt = h.intersection(v)
            if type(int_pt) is Point:
                horizontal_points.append((int(int_pt.x), int(int_pt.y)))
        result_points.append(horizontal_points)
        horizontal_points = []
    return result_points


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return int(x), int(y)


def create_lines_from_points(points1: list[int], points2: list[int], horizontal, max_val) -> list[LineString]:
    if len(points1) != len(points2):
        raise ValueError('points are not matching')
    optimal_lines = []
    for i in range(len(points1)):
        if horizontal:
            optimal_lines.append(LineString([[0, int(points1[i])], [max_val, int(points2[i])]]))
        else:
            optimal_lines.append(LineString([[int(points1[i]), 0], [int(points2[i]), max_val]]))
    return optimal_lines


def grid_lines_from_points(points1: list, points2: list, horizontal: bool, width: int, height: int) -> list[LineString]:
    if points1 is None or points2 is None or len(points1) != len(points2):
        return []
    if horizontal:
        sorted_lines = create_lines_from_points(points1, points2, horizontal, width)
    else:
        sorted_lines = create_lines_from_points(points1, points2, horizontal, height)
    return sorted_lines


def line_scanner_hough(template: Template):
    template_grey = template.image_grey.copy()
    img_grey = cv2.bitwise_not(template_grey)

    lines = cv2.HoughLinesP(
        img_grey,  # Input edge image
        cv2.HOUGH_PROBABILISTIC,
        np.pi / 180,  # Angle resolution in radians
        threshold=100,  # Min number of votes for valid line
        minLineLength=250,  # Min allowed length of line
        maxLineGap=3  # Max allowed gap between line for joining them
    )

    # Iterate over points
    lines_list = []
    for edges in lines:
        # Extracted points nested in the list
        x1, y1, x2, y2 = edges[0]
        lines_list.append(LineString([(x1, y1), (x2, y2)]))
    return lines_list
