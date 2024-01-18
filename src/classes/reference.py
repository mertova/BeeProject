from pathlib import Path
from cv2 import imread, IMREAD_GRAYSCALE


class Reference:
    def __init__(self, path: Path):
        if not path.exists() or not path.is_file():
            raise FileNotFoundError("template file does not exists")
        self.path = path
        self.image_grey = imread(path.as_posix(), IMREAD_GRAYSCALE)
        self.image_color = imread(path.as_posix())

    def __str__(self):
        return f"{self.path}"
