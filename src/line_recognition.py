import cv2
import numpy as np


def detect_lines_hough(gray):
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    # Second, process edge detection use Canny.
    low_threshold = 50
    high_threshold = 300
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    # Then, use HoughLinesP to get the lines. You can adjust the parameters for better performance.

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    return lines


def write_lines(image, lines):
    line_image = np.copy(image) * 0  # creating a blank to draw lines on
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 3)

    return line_image
