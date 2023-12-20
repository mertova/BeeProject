
import numpy as np
import cv2
import lineUtils
import pointUtils
from shapely.geometry import LineString, Polygon
import random


template = cv2.imread('../data/templates/template.png')
results_path = '../data/results/line_recognition/results/'


def find_border_points(lines, eps_h, eps_v):
    if lines is None or len(lines) == 0:
        return
    template_copy = template.copy()

    # up, down, left, right
    intersections_borders = [[], [], [], []]
    for line in lines:
        if line is not None:
            for i in range(4):
                intersect = lineUtils.two_infinite_lines_intersection(line, borders[i], width, height)
                if intersect is not None:
                    template_copy = cv2.circle(template_copy, intersect, radius=5, color=(255, 128, 0), thickness=-1)
                    if i < 2:
                        intersections_borders[i].append(intersect[0])
                    else:
                        intersections_borders[i].append(intersect[1])
    clustered_points = []
    template_copy = lineUtils.write_lines(template_copy, borders, (0, 153, 0))
    for i in range(len(intersections_borders)):
        if i < 2:
            optimal_points = pointUtils.clustering_eps(intersections_borders[i], 12)
            optimal_points.append(width)
            optimal_points.append(0)
        else:
            optimal_points = pointUtils.clustering_eps(intersections_borders[i], 7)
            optimal_points.append(height)
            optimal_points.append(0)
        clustered_points.append(sorted(optimal_points))
        print("optimal points: ")
        print(optimal_points)
    cv2.imwrite(results_path + 'optimal_border_intersections_template.png', template_copy)
    return clustered_points


def draw_lines(points1, points2, horizontal):
    if points1 is None or points2 is None or len(points1) != len(points2):
        return []
    if horizontal:
        sorted_lines = lineUtils.create_lines_from_points(points1, points2, horizontal, width)
    else:
        sorted_lines = lineUtils.create_lines_from_points(points1, points2, horizontal, height)
    return sorted_lines


def bounding_boxes_form_points(p: [[(int, int)]]):
    if p is None or len(p) == 0:
        return None
    template_copy = template.copy()
    boxes = []
    for i in range(len(p) - 1):
        sorted_points1 = sorted(p[i], key=lambda x: (x[0], x[1]))
        sorted_points2 = sorted(p[i+1], key=lambda x: (x[0], x[1]))
        print(sorted_points1)
        print(sorted_points2)
        if len(sorted_points1) != len(sorted_points2):
            raise ValueError('Bounding boxes must have the same number of points')
        for j in range(len(sorted_points1) - 1):
            boxes.append(Polygon((sorted_points1[j],
                                  sorted_points1[j+1],
                                  sorted_points2[j],
                                  sorted_points2[j+1])
                                 ))
            cv2.rectangle(template_copy, sorted_points1[j], sorted_points2[j + 1], (random.randint(0, 255),
                                                                                    random.randint(0, 255),
                                                                                    random.randint(0, 255)), -1)
    cv2.imwrite(results_path + "boxes.png", template_copy)
    return boxes


def line_scanner_hough():
    template_grey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    img_grey = cv2.bitwise_not(template_grey)
    cv2.imwrite(results_path + "preprocessing_template.png", img_grey)

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
    template_copy = template.copy()
    for edges in lines:
        # Extracted points nested in the list
        x1, y1, x2, y2 = edges[0]
        pt1 = (x1, y1)
        pt2 = (x2, y2)
        cv2.circle(template_copy, pt1, 3, (15, 49, 100), 3)
        cv2.circle(template_copy, pt1, 3, (15, 49, 100), 3)
        cv2.line(template_copy, pt1, pt2, (0, 255, 0), 2)
        lines_list.append((pt1, pt2))
    cv2.imwrite(results_path + "hough_lines.png", template_copy)
    return lines_list


if __name__ == '__main__':
    # definition of the template shape
    height, width = template.shape[:2]
    up_left = (0, 0)
    up_right = (width, 0)
    down_left = (0, height)
    down_right = (width, height)
    borders = [(up_left, up_right), (down_left, down_right), (up_left, down_left), (up_right, down_right)]

    # line recognition with hough algorithm
    h_lines = line_scanner_hough()

    # todo filter all not vertical or horizontal lines

    # get ordered positions with all borderlines - clustered
    points = find_border_points(h_lines, 15, 20)

    # write lines
    template1 = template.copy()
    grid_lines_vertical = draw_lines(points[0], points[1], False)
    template1 = lineUtils.write_lines(template1, grid_lines_vertical, (0, 255, 60))

    grid_lines_horizontal = draw_lines(points[2], points[3], True)
    template1 = lineUtils.write_lines(template1, grid_lines_horizontal, (200, 0, 60))
    cv2.imwrite(results_path + 'lines.png', template1)

    # intersections of all lines
    intersections = lineUtils.calculate_intersections(grid_lines_horizontal, grid_lines_vertical)
    for intersection in intersections:
        template1 = pointUtils.write_points(template1, intersection, (0, 0, 180))

    # Save the result image - detected lines and intersections
    cv2.imwrite(results_path + 'lines_template.png', template1)

    # create bounding boxes of all cells
    boxes = bounding_boxes_form_points(intersections)
    print(boxes)


