import cv2
from geometry.vertex import Vertex


class Rectangle:
    pt2: Vertex | None
    pt1: Vertex | None
    center: Vertex | None

    text: str | None

    def __init__(self, pt1: Vertex, pt2: Vertex, text: str):
        self.pt1 = pt1
        self.pt2 = pt2
        self.center = None
        self.text = text

    def calculate_center(self):
        x = int((self.pt1.x + self.pt2.x) / 2)
        y = int((self.pt1.y + self.pt2.y) / 2)
        self.center = Vertex(x, y)

    def contains_point(self, pt: Vertex) -> bool:
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        return x1 <= pt.x <= x2 and y1 <= pt.y <= y2

    def render(self, canvas, with_text: bool = False):
        """
        Draw rectangle on canvas with given text.
        :param with_text: weather text should be included
        :param canvas: canvas to draw rectangle on
        :return: image with rectangle and text on it
        """
        rec_color = (0, 140, 255)
        text_color = (0, 0, 0)
        cv2.rectangle(canvas, self.pt1.as_tuple(), self.pt2.as_tuple(), rec_color, 3)
        left_bottom = (int(self.pt1.x) +30, int(self.pt2.y) - 10 )
        if with_text:
            text = self.text
            canvas = cv2.putText(canvas, text, left_bottom,
                                 cv2.FONT_HERSHEY_SIMPLEX, 1, text_color,
                                 2, cv2.LINE_AA, False)
        return canvas

    def crop_image(self, image):
        if self.pt1.is_more_than(self.pt2, 0.1):
            height = self.pt1.y - self.pt2.y
            width = self.pt1.x - self.pt2.x
            first = self.pt2
        else:
            height = self.pt2.y - self.pt1.y
            width = self.pt2.x - self.pt1.x
            first = self.pt1
        return image[first.y: first.y + height, first.x: first.x + width]
