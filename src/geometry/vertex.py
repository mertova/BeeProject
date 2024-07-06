import cv2


class Vertex:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def is_more_than(self, other, eps):
        if self.x - eps > other.x and self.y - eps > other.y:
            return True
        return False

    def as_tuple(self):
        return self.x, self.y

    def render(self, img, color, radius=5):
        return cv2.circle(img, self.as_tuple(), radius, color=color, thickness=-1)

    def __dict__(self):
        return {'x': self.x, 'y': self.y}

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

