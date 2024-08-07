import cv2

from geometry.vertex import Vertex


class Line:
    pt1: Vertex
    pt2: Vertex

    vector: tuple

    def __init__(self, pt1: Vertex, pt2: Vertex):
        self.pt1 = pt1
        self.pt2 = pt2
        self.set_vector()

    def set_vector(self):
        """
        (point 2 - point 1)
        """
        self.vector = (self.pt2.x - self.pt1.x), (self.pt2.y - self.pt1.y)

    def intersects(self, other):
        """
        Find point of intersection of self and other line both defined by 2 point
        :param other: other line
        :return: Vertex if line intersects with other line else None
        """
        max_x = max(self.pt1.x, self.pt2.x, other.pt1.x, other.pt2.x)
        min_x = min(self.pt1.x, self.pt2.x, other.pt1.x, other.pt2.x)
        max_y = max(self.pt1.y, self.pt2.y, other.pt1.y, other.pt2.y)
        min_y = min(self.pt1.y, self.pt2.y, other.pt1.y, other.pt2.y)

        if self.vector[0] == 0 and other.vector[0] == 0:
            # lines are vertical and parallel
            return None

        if self.vector[0] == 0:
            slope = other.vector[1] / other.vector[0]
            c = other.pt1.y - slope * other.pt1.x
            x = self.pt1.x
            y = slope * x + c
        elif other.vector[0] == 0:
            slope = self.vector[1] / self.vector[0]
            c = self.pt1.y - slope * self.pt1.x
            x = other.pt1.x
            y = slope * x + c
        else:
            slope1 = self.vector[1] / self.vector[0]
            slope2 = other.vector[1] / other.vector[0]
            c1 = self.pt1.y - slope1 * self.pt1.x
            c2 = other.pt1.y - slope2 * other.pt1.x
            if slope1 == slope2:
                return None
            x = (c2 - c1) / (slope1 - slope2)
            y = slope1 * x + c1

        if min_x <= x <= max_x and min_y <= y <= max_y:
            x = round(x, 2)
            y = round(y, 2)
            return Vertex(x, y)
        return None

    def point_within(self, point: Vertex):
        """
        true is point within this line
        :param point: Vertex to check
        :return: true if point is within this line
        """
        if point is None:
            return False
        t1 = (point.x - self.pt1.x) / self.vector[0]
        t2 = (point.y - self.pt1.y) / self.vector[1]
        return t1 == t2

    def line_set_intersections(self, l_set: list, vertical: bool) -> list:
        """
        Vertex coordinates of the intersection of line with self
        :param l_set: input line set
        :param vertical: true if line is vertical, else horizontal
        :return: false if no intersection (determinant == 0)
        """
        if self is None or l_set is None:
            return []
        results = []
        for line in l_set:
            int_pt = self.intersects(line)
            if int_pt is not None:
                if vertical:
                    results.append(int_pt.y)
                else:
                    results.append(int_pt.x)
        return results

    def render(self, img, color):
        p1 = self.pt1.as_tuple()
        p2 = self.pt2.as_tuple()
        img = cv2.line(img, p1, p2, color, 2)
        return img

    def __str__(self):
        return f'Line({self.pt1}, {self.pt2})'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.pt1 == other.pt1 and self.pt2 == other.pt2

    def __hash__(self):
        return hash((self.pt1, self.pt2))
