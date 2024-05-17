import cv2
from geometry.vertex import Vertex


class Rectangle:
    pt2: Vertex | None
    pt1: Vertex | None

    def __init__(self, pt1: Vertex, pt2: Vertex):
        self.pt1 = pt1
        self.pt2 = pt2
        self.centre = None
        if self.pt1 is not None or self.pt2 is not None:
            self.centre = (self.pt1.x + self.pt2.x)/2, (self.pt1.y + self.pt2.y)/2

    def render(self, canvas, text):
        rec_color = (0, 255, 60)
        text_color = (200, 0, 60)
        canvas = cv2.rectangle(canvas, self.pt1.as_tuple(), self.pt2.as_tuple(), rec_color, 2)
        canvas = cv2.putText(canvas, text, self.centre,
                             cv2.FONT_HERSHEY_SIMPLEX, 1, text_color,
                             2, cv2.LINE_AA, True)
        return canvas

    def point_is_inside(self, pt: Vertex) -> bool:
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        return x1 <= pt.x <= x2 and y1 <= pt.y <= y2
