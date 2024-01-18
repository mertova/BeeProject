from pathlib import Path
from cv2 import Mat, imread, IMREAD_GRAYSCALE


class Template:
    def __init__(self, name: str, path: Path, img_grey: Mat):
        if not path.exists() or not path.is_file():
            raise FileNotFoundError("template file does not exists")
        self.name = name
        self.path = path
        self.image_grey = img_grey
        self.width, self.height, _ = self.image_grey.shape

    def __str__(self):
        return f"{self.path}({self.name})"
