import cv2


def test_input(n):
    # todo
    try:
        n = int(n)
    except ValueError:
        raise ValueError("vertex coordinate must be an integer")
    return n


class Vertex:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = test_input(x)
        self.y = test_input(y)

    def is_more_than(self, other):
        """
        Checks if the vertex coordinates are less than the other vertex coordinates.First check x coordinates, then y.
        :param other: Other vertex
        :return: True is self.x is more than other.x. If x coordinates are equal, check if y coordinates are more than
        other.y
        """
        if self.x > other.x:
            return True
        if self.x == other.x:
            return self.y > other.y
        return False

    def as_tuple(self):
        """
        Converts the vertex coordinates to a tuple
        :return: vertex coordinates (x, y)
        """
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

