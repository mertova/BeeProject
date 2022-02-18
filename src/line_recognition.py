import numpy as np
from cv2 import cv2
from shapely.geometry import LineString, Point, box, Polygon


# expects all images same shape!
def sum_canny(images: list):
    if (images is None) | (len(images) == 0):
        return None

    # Second, process edge detection use Canny.
    low_threshold = 50
    high_threshold = 300
    sum_image = images[0] * 0

    kernel_size = 5

    for image in images:
        edges = cv2.Canny(cv2.GaussianBlur(image, (kernel_size, kernel_size), 0), low_threshold, high_threshold)
        thresh1, edges = cv2.threshold(edges, 127, 1, cv2.THRESH_BINARY)
        sum_image += edges

    return sum_image, len(images)


def detect_lines_hough(template):
    # img = cv2.cvtColor(template, cv2.COLOR_GRAY2RGB)

    # Then, use HoughLinesP to get the lines. You can adjust the parameters for better performance.
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 80  # 15 minimum number of votes (intersections in Hough grid cell)
    min_line_length = 400  # 50 minimum number of pixels making up a line
    max_line_gap = 10  # 20 maximum gap in pixels between connectable line segments

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(template, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    return lines


def make_lines_infinite(lines, height, width):
    i = 0
    new_lines = []
    for line in lines:
        new_lines.append(infinite_line(LineString([[line[0][0], line[0][1]], [line[0][2], line[0][3]]]), height, width))
    return new_lines


# lines are LineString
def reduce_lines(lines: list[LineString]):
    new_lines = []

    reduce_lines_recursive(lines, 0)
    return new_lines


# todo rewrite
def reduce_lines_recursive(lines: list[LineString], length: int):
    if len(lines) <= 2 | len(lines) == length:
        return lines

    reduced = lines.copy()
    for i in range(len(lines)-1):
        for j in range(i+1, len(lines)):
            if lines[i].distance(lines[j]) < 5:
                reduced.pop(i)
                reduced.pop(j)
                reduced.append(calculate_middle_line(lines[i], lines[j]))
                return reduce_lines_recursive(reduced, len(lines))

    return reduced


def infinite_line(line: LineString, height, width):
    minx = 0
    miny = 0
    maxx = width
    maxy = height
    bounding_box = box(minx, miny, maxx, maxy)
    a, b = line.xy
    if a[0] == b[0]:  # vertical line
        extended_line = LineString([(a.x, miny), (a.x, maxy)])
    elif a[1] == b[1]:  # horizonthal line
        extended_line = LineString([(minx, a.y), (maxx, a.y)])
    else:
        # linear equation: y = k*x + m
        k = (b[1] - a[1]) / (b[0] - a[0])
        m = a[1] - k * a[0]
        y0 = k * minx + m
        y1 = k * maxx + m
        x0 = (miny - m) / k
        x1 = (maxy - m) / k
        points_on_boundary_lines = [Point(minx, y0), Point(maxx, y1),
                                    Point(x0, miny), Point(x1, maxy)]
        points_sorted_by_distance = sorted(points_on_boundary_lines, key=bounding_box.distance)
        extended_line = LineString(points_sorted_by_distance[:2])
    return extended_line


def calculate_middle_line(line1: LineString, line2: LineString) -> LineString:
    first1, last1 = line1.xy
    first2, last2 = line2.xy

    if abs(first1[0] - first2[0]) < abs(first1[0] - last2[0]):
        x1 = min(first1[0], first2[0]) + abs(first1[0] - first2[0])/2
    else:
        x1 = min(first1[0], last2[0]) + abs(first1[0] - last2[0])/2

    if abs(first1[1] - first2[1]) < abs(first1[1] - last2[1]):
        y1 = min(first1[1], first2[1]) + abs(first1[1] - first2[1])/2
    else:
        y1 = min(first1[1], last2[1]) + abs(first1[1] - last2[1])/2

    if abs(last1[0] - first2[0]) < abs(last1[0] - last2[0]):
        x2 = min(last1[0] - first2[0]) + abs(last1[0] - first2[0])/2
    else:
        x2 = min(last1[0], last2[0]) + abs(last1[0] - last2[0])/2

    if abs(last1[1] - first2[1]) < abs(last1[1] - last2[1]):
        y2 = min(last1[1], first2[1]) + abs(last1[1] - first2[1])/2
    else:
        y2 = min(last1[1], last2[1]) + abs(last1[1] - last2[1])/2

    return LineString([[x1, y1], [x2, y2]])


def write_lines(image, lines: list[LineString]):
    line_image = np.copy(image) * 0  # creating a blank to draw lines on
    for line in lines:
        first, last = line.xy
        cv2.line(line_image, (int(first[0]), int(first[1])), (int(last[0]), int(last[1])), (255, 0, 0), 2)

    return line_image


def write_points(image, points):
    for point in points:
        cv2.circle(image, (point[0], point[1]), radius=5, color=(255, 255, 0), thickness=-1)
    return image


def preprocessing(template):
    template = cv2.GaussianBlur(template, (3, 3), 0)
    img = cv2.adaptiveThreshold(template, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 75, 10)
    img = cv2.bitwise_not(img)
    return img


# x,y coordinates of the intersection of two input lines
# false if no intersection (determinant == 0)
def calculate_intersections(lines):
    result_points = []

    for line1 in lines:
        for line2 in lines:
            int_pt = line1.intersection(line2)
            if not int_pt.is_empty:
                result_points.append([int(int_pt.x), int(int_pt.y)])

    return result_points


# Load image, convert to grayscale, threshold and find contours
# then apply fitline() function
def fit_line_cv2(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, hier = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]

    [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)

    # Now find two extreme points on the line to draw line
    lefty = int((-x * vy / vx) + y)
    righty = int(((gray.shape[1] - x) * vy / vx) + y)

    # Finally draw the line
    cv2.line(image, (gray.shape[1] - 1, righty), (0, lefty), 255, 2)
    return image
