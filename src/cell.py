from shapely import Polygon
import json


def decoding_identifier(ident: str):
    letter = ident[0]
    number = ident[1:]
    column = ord(letter) - ord('A')
    row = int(number)
    return column, row


class Cell:
    def __init__(self, pt1: (int, int), pt2: (int, int), row_id: int, col_id: int, polygon: Polygon):
        self.annotation = None
        self.pt1 = pt1
        self.pt2 = pt2
        self.area = polygon.area
        self.row_id = row_id
        self.col_id = col_id

    def __str__(self):
        if self.annotation is not None:
            return f"{chr(ord('A') + self.col_id)}{self.row_id}: {self.annotation}"

    def __gt__(self, cell2):
        if self.row_id == cell2.row_id:
            return self.col_id > cell2.col_id
        return self.row_id > cell2.row_id

    def __eq__(self, other):
        return self.row_id == other.row_id and self.col_id == other.col_id

    """
    Returns a string representation -json of the coords and identifier
    :return:
    """
    """    def __repr__(self):

        pass"""

    def annotate(self, annotation: str):
        if annotation is not None and annotation.endswith("\n"):
            annotation = annotation[:-1]
        self.annotation = annotation

    def as_dict(self):
        return {'id': str(self.row_id) + '-' + str(self.col_id), 'annotation': self.annotation,
                'pt1': self.pt1, 'pt2': self.pt2}
