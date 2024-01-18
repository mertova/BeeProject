import cv2
import numpy as np
from shapely.geometry import LineString, Point


# x,y coordinates of the intersection of two input lines
# false if no intersection (determinant == 0)
def calculate_intersections(horizontal: list[LineString], vertical: list[LineString]) -> list[list[(int, int)]]:
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


# write lines to the image
def write_lines(image, lines: list, color):
    if lines is None:
        return image
    for line in lines:
        if type(line) is tuple:
            pt1, pt2 = line
            cv2.line(image, pt1, pt2, color, 4)
        elif type(line) is LineString:
            # pt1 = tuple(map(int, line.xy[0]))
            # pt2 = tuple(map(int, line.xy[1]))
            pt1 = (int(line.xy[0][0]), int(line.xy[1][0]))
            pt2 = (int(line.xy[0][1]), int(line.xy[1][1]))
            cv2.line(image, pt1, pt2, color, 4)
    return image


def two_infinite_lines_intersection(line1, line2, width, height):
    p1_start = np.asarray(line1[0])
    p1_end = np.asarray(line1[1])
    p2_start = np.asarray(line2[0])
    p2_end = np.asarray(line2[1])

    r = (p1_end - p1_start)
    s = (p2_end - p2_start)
    c1 = np.cross(r, s)
    c2 = np.cross(p2_start - p1_start, s)
    if c1 == 0:
        return None
    t = c2 / c1
    x = p1_start[0] + r[0] * t
    y = p1_start[1] + r[1] * t
    i = (int(x), int(y))
    if i is not None and 0 <= i[0] <= width and 0 <= i[1] <= height:
        return i[0], i[1]
    return None


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


def draw_lines(points1, points2, horizontal, width, height):
    if points1 is None or points2 is None or len(points1) != len(points2):
        return []
    if horizontal:
        sorted_lines = create_lines_from_points(points1, points2, horizontal, width)
    else:
        sorted_lines = create_lines_from_points(points1, points2, horizontal, height)
    return sorted_lines
