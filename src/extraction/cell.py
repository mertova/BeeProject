from shapely import Polygon


def decoding_identifier(ident: str):
    letter = ident[0]
    number = ident[1:]
    column = ord(letter) - ord('A')
    row = int(number)
    return column, row


class Cell:
    def __init__(self, row_id: int, col_id: int, pt1: (int, int), pt2: (int, int), pt3: (int, int), pt4: (int, int)):
        self.row_id = row_id
        self.col_id = col_id
        self.pt1 = pt1
        self.pt2 = pt2
        self.pt3 = pt3
        self.pt4 = pt4
        self.polygon = Polygon((pt1, pt2, pt3, pt4))
        self.annotation = None

    def __str__(self):
        if self.annotation is not None:
            return f"{chr(ord('A') + self.col_id)}{self.row_id}: {self.annotation}"
        else:
            return f"{chr(ord('A') + self.col_id)}{self.row_id}"

    def __gt__(self, cell2):
        if self.row_id == cell2.row_id:
            return self.col_id > cell2.col_id
        return self.row_id > cell2.row_id

    def __eq__(self, other):
        return self.row_id == other.row_id and self.col_id == other.col_id

    def annotate(self, annotation: str):
        if annotation is not None and annotation.endswith("\n"):
            annotation = annotation[:-1]
        self.annotation = annotation

    def as_dict(self):
        """
        dictionary representation of the cell
        :return Returns a string representation (-json) of the coords and identifier
        """
        return {'id_row': str(self.row_id), 'id_col': str(self.col_id), 'pt1': self.pt1, 'pt2': self.pt2,
                'pt3': self.pt3, 'pt4': self.pt4, 'annotation': self.annotation}

    def get_area(self):
        return self.polygon.area
