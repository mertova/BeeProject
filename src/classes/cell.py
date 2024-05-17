from geometry.rectangle import Rectangle
from geometry.vertex import Vertex


class Cell(Rectangle):
    """
    Represents a region of interest - classes cell - that was found in the template
    """
    row_id: int
    col_id: int
    is_active: bool
    id: str

    def __init__(self, row_id: int = None, col_id: int = None, pt1: Vertex = None, pt2: Vertex = None):
        super().__init__(pt1, pt2)
        self.row_id = row_id
        self.col_id = col_id
        self.id = self.encode_index()
        self.is_active = False

    def __dict__(self):
        """
        dictionary representation of the cell
        :return Returns a string representation (-json) of the coords and identifier
        """
        return {'id': self.id, 'pt1': self.pt1, 'pt2': self.pt2}

    def import_json(self, json_dict):
        self.id = json_dict['id']
        self.pt1 = Vertex(json_dict['pt1'][0], json_dict['pt1'][1])
        self.pt2 = Vertex(json_dict['pt2'][0], json_dict['pt2'][1])
        self.col_id, self.row_id = self.decode_index()
        self.row_id = int(json_dict['id_row'])

    def decode_index(self):
        letter = self.id[0]
        number = self.id[1:]
        column = ord(letter) - ord('A')
        row = int(number)
        return column, row

    def encode_index(self):
        if self.col_id is not None and self.row_id is not None:
            letter = chr(ord('A') + self.col_id)
            return letter + str(self.row_id)
        return None

    def activate_cell(self):
        self.is_active = True

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
