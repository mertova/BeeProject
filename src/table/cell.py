from geometry.vertex import Vertex


def decode_index(index):
    letter = index[0]
    number = index[1:]
    column = ord(letter) - ord('A')
    row = int(number)
    return column, row


class Cell:
    """
    Represents a region of interest that was found in the template
    """
    row_id: int | None
    col_id: int | None
    is_active: bool
    pt2: Vertex | None
    pt1: Vertex | None

    def __init__(self, row_id: int = None, col_id: int = None, pt1: Vertex = None, pt2: Vertex = None):
        self.row_id = row_id
        self.col_id = col_id
        self.id = self.encode_index()
        self.pt1 = pt1
        self.pt2 = pt2
        self.is_active = False

    def export_dict(self):
        """
        dictionary representation of the cell
        :return Returns a string representation (-json) of the coords and identifier
        """
        return {'id': self.id, 'id_row': str(self.row_id), 'id_col': str(self.col_id), 'pt1': self.pt1,
                'pt2': self.pt2}

    def import_json(self, json_dict):
        self.id = json_dict['id']
        self.pt1 = Vertex(json_dict['pt1'][0], json_dict['pt1'][1])
        self.pt2 = Vertex(json_dict['pt2'][0], json_dict['pt2'][1])
        self.col_id = int(json_dict['id_col'])
        self.row_id = int(json_dict['id_row'])

    def encode_index(self):
        if self.col_id is not None and self.row_id is not None:
            letter = chr(ord('A') + self.col_id)
            return letter + str(self.row_id)
        return None

    def activate_cell(self):
        self.is_active = True

    def rectangle_is_inside(self, pt1: Vertex, pt2: Vertex, eps):
        if not self.pt1.is_more_than(pt1, eps) and self.pt2.is_more_than(pt2, eps):
            return True
        return False

    def point_is_inside(self, pt: Vertex) -> bool:
        x1 = self.pt1.x
        y1 = self.pt1.y
        x2 = self.pt2.x
        y2 = self.pt2.y
        return x1 <= pt.x <= x2 and y1 <= pt.y <= y2

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return f"{self.id}"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __gt__(self, cell2):
        if self.col_id == cell2.col_id:
            return self.row_id > cell2.row_id
        return self.col_id > cell2.col_id
