import numpy as np
import cv2

from geometry.line import Line
from geometry.vertex import Vertex
from image_processing.image import Image


class Form(Image):
    __height: int
    __width: int

    __up_left: Vertex
    __up_right: Vertex
    __down_left: Vertex
    __down_right: Vertex

    __border_up: Line
    __border_down: Line
    __border_left: Line
    __border_right: Line

    def __init__(self, image: str):
        super().__init__(image)
        self.__set_dimensions()

    def __set_dimensions(self):
        """
        set dimensions of the form image: width, height, 4 corner points and 4 borderlines from the sape of the image
        """
        self.height, self.width = self._grey.shape

        self._up_left = Vertex(0, 0)
        self._up_right = Vertex(self.width, 0)
        self._down_left = Vertex(0, self.height)
        self._down_right = Vertex(self.width, self.height)

        self._border_up = Line(self._up_left, self._up_right)
        self._border_down = Line(self._down_left, self._down_right)
        self._border_left = Line(self._up_left, self._down_left)
        self._border_right = Line(self._up_right, self._down_right)

    def get_border_up(self):
        return self._border_up

    def get_border_down(self):
        return self._border_down

    def get_border_left(self):
        return self._border_left

    def get_border_right(self):
        return self._border_right

    def line_scanner_hough(self):
        """
        Hough line scanner
        :return: List of geometry.line.Line
        """
        lines = cv2.HoughLinesP(
            self._inverse,  # Input edge image
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
            v1 = Vertex(x1, y1)
            v2 = Vertex(x2, y2)
            lines_list.append(Line(v1, v2))
        return lines_list

