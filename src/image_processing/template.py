from pathlib import Path

import numpy as np
import cv2

from geometry.line import Line
from image_processing import preprocessing
from image_processing.image import Image


class Template(Image):
    path: Path

    height: int = None
    width: int = None
    border_lines = None

    def __init__(self, image: str):
        super().__init__(cv2.imread(image))

        if template_img is None:
            self.load_img_from_path()

        self.set_template_dimensions()
        self.set_template_borders()

    def line_scanner_hough(self):
        lines = cv2.HoughLinesP(
            self.get_negative_grey,  # Input edge image
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
            lines_list.append(Line([(x1, y1), (x2, y2)]))
        return lines_list

    def set_template_dimensions(self):
        self.height, self.width = self.grey.shape

    def set_template_borders(self):
        """
        creates 4 borderlines from the sape of the image
        :return:
        """
        up_left = [0, 0]
        up_right = [self.width, 0]
        down_left = [0, self.height]
        down_right = [self.width, self.height]
        self.borders = [LineString([up_left, up_right]), LineString([down_left, down_right]),
                        LineString([up_left, down_left]), LineString([up_right, down_right])]

    def dump_template(self):
        cv2.imwrite(self.path.as_posix(), self.image_grey)