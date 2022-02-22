import numpy as np
from cv2 import cv2
from shapely.geometry import LineString, Point, box, Polygon
from src import lineUtils


def preprocessing(template):
    template = cv2.GaussianBlur(template, (3, 3), 0)
    img = cv2.adaptiveThreshold(template, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 75, 10)
    img = cv2.bitwise_not(img)
    return img


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

    results = []
    for line in lines:
        results.append(LineString([(line[0][0], line[0][1]), (line[0][2], line[0][3])]))
    return results


def make_lines_infinite(lines, height, width):
    new_lines = []
    for line in lines:
        new_lines.append(lineUtils.infinite_line(line, height, width))
    return new_lines


# todo rewrite
def reduce_lines_recursive(lines: list[LineString], length: int):
    if len(lines) <= 2 | len(lines) == length:
        return lines

    reduced = lines.copy()
    pop = []
    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            if lines[i].difference(lines[j]):
                # pop.append((i, j))
                if reduced.__contains__(lines[j]):
                    reduced.remove(lines[j])
                # reduced.pop(j)
                # reduced.append(calculate_middle_line(lines[i], lines[j]))
                # return reduce_lines_recursive(reduced, len(lines))

    for item in pop:
        print(item)
    return reduced


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
