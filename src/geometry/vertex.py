class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_more_than(self, other, eps):
        if self.x - eps > other.x and self.y - eps > other.y:
            return True
        return False

    def as_tuple(self):
        return self.x, self.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'

