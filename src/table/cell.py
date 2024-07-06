from geometry.rectangle import Rectangle
from geometry.vertex import Vertex


def decode_index(code):
    letter = code[0]
    number = code[1:]
    column = ord(letter) - ord('A')
    row = int(number)
    return column, row


def encode_index(col, row):
    if col is not None and row is not None:
        letter = chr(ord('A') + col)
        return letter + str(row)
    return None


class Cell(Rectangle):
    """
    Represents a region of interest - classes cell - that was found in the template
    Text inherited from Rectangle is encoded index - row and column ids
    """
    row_id: int
    col_id: int
    is_active: bool

    def __init__(self, row_id: int = None, col_id: int = None, pt1: Vertex = None, pt2: Vertex = None):
        self.row_id = row_id
        self.col_id = col_id
        self.is_active = False
        super().__init__(pt1, pt2, encode_index(self.col_id, self.row_id))

    def __dict__(self):
        """
        dictionary representation of the cell
        :return Returns a string representation (-json) of the coords and identifier
        """
        return {'text': self.text, 'pt1': self.pt1.__dict__(), 'pt2': self.pt2.__dict__()}

    def import_json(self, json_dict):
        self.text = json_dict['text']
        self.pt1 = Vertex(json_dict['pt1']['x'], json_dict['pt1']['y'])
        self.pt2 = Vertex(json_dict['pt2']['y'], json_dict['pt2']['y'])
        self.col_id, self.row_id = decode_index(self.text)

    def activate_cell(self):
        self.is_active = True

    def __str__(self):
        return f"{self.text}"

    def __repr__(self):
        return f"{self.text}"

    def __eq__(self, other):
        return self.col_id == other.col_id and self.row_id == other.row_id

    def __hash__(self):
        return hash((self.col_id, self.row_id))

    def __gt__(self, cell2):
        if self.col_id == cell2.col_id:
            return self.row_id > cell2.row_id
        return self.col_id > cell2.col_id
