from cv2 import cv2
import numpy as np
from shapely.geometry import LineString, box, Point


# extend line to the borders of the image
def infinite_line(line: LineString, maxy: int, maxx: int):
    minx = 0
    miny = 0
    bounding_box = box(minx, miny, maxx, maxy)
    a, b = line.xy
    if a[0] == b[0]:  # vertical line
        extended_line = LineString([(a[0], a[0]), (miny, maxy)])
    elif a[1] == b[1]:  # horizontal line
        extended_line = LineString([(minx, maxx), (a[1], a[1])])
    else:
        # linear equation: y = k*x + m
        k = (b[1] - a[1]) / (b[0] - a[0])
        m = a[1] - k * a[0]
        y0 = k * minx + m
        y1 = k * maxx + m
        x0 = (miny - m) / k
        x1 = (maxy - m) / k
        points_on_boundary_lines = [Point(minx, maxx), Point(y0, y1),
                                    Point(x0, x1), Point(miny, maxy)]
        points_sorted_by_distance = sorted(points_on_boundary_lines, key=bounding_box.distance)
        extended_line = LineString(points_sorted_by_distance[:2])
    return


# x,y coordinates of the intersection of two input lines
# false if no intersection (determinant == 0)
def calculate_intersections(lines: list[LineString]):
    result_points = set()

    for line1 in lines:
        for line2 in lines:
            int_pt = line1.intersection(line2)
            if type(int_pt) == Point:
                result_points.add((int(int_pt.x), int(int_pt.y)))

    return result_points


# todo
def calculate_middle_line(line1: LineString, line2: LineString) -> LineString:
    first1, last1 = line1.xy
    first2, last2 = line2.xy

    if abs(first1[0] - first2[0]) < abs(first1[0] - last2[0]):
        x1 = min(first1[0], first2[0]) + abs(first1[0] - first2[0]) / 2
    else:
        x1 = min(first1[0], last2[0]) + abs(first1[0] - last2[0]) / 2

    if abs(first1[1] - first2[1]) < abs(first1[1] - last2[1]):
        y1 = min(first1[1], first2[1]) + abs(first1[1] - first2[1]) / 2
    else:
        y1 = min(first1[1], last2[1]) + abs(first1[1] - last2[1]) / 2

    if abs(last1[0] - first2[0]) < abs(last1[0] - last2[0]):
        x2 = min(last1[0] - first2[0]) + abs(last1[0] - first2[0]) / 2
    else:
        x2 = min(last1[0], last2[0]) + abs(last1[0] - last2[0]) / 2

    if abs(last1[1] - first2[1]) < abs(last1[1] - last2[1]):
        y2 = min(last1[1], first2[1]) + abs(last1[1] - first2[1]) / 2
    else:
        y2 = min(last1[1], last2[1]) + abs(last1[1] - last2[1]) / 2

    return LineString([[x1, y1], [x2, y2]])


# write lines to the image
def write_lines(image, lines: list[LineString]):
    for line in lines:
        first, last = line.xy
        cv2.line(image, (int(first[0]), int(last[0])), (int(first[1]), int(last[1])), (255, 0, 0), 2)

    return image
