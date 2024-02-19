from pathlib import Path

import cv2
from shapely import LineString
from pdf2image import convert_from_path


class Image:

    def __init__(self, path: Path):
        if not path.exists() or not path.is_file():
            raise FileExistsError("file does not exists")
        self.path = path
        self.name = path.name

        if self.name.endswith('.pdf'):
            images = convert_from_path(path)
            if len(images) != 1:
                raise FileExistsError("pdf file " + path.name + " has several pages. 1 PDF page is required.")
            self.image_color = images[0]
        elif self.name.endswith('.jpg') or self.name.endswith('.png'):
            self.image_color = cv2.imread(self.path.as_posix())
        else:
            raise FileNotFoundError("Unsupported file type")

        self.image_grey = cv2.cvtColor(self.image_color, cv2.COLOR_BGR2GRAY)
        self.height, self.width = self.image_grey.shape
        self.borders = self.borders()

    def __str__(self):
        return f"{self.path}({self.name})"

    def borders(self) -> list[LineString]:
        """
        creates 4 borderlines from the sape of the image
        :return:
        """
        up_left = [0, 0]
        up_right = [self.width, 0]
        down_left = [0, self.height]
        down_right = [self.width, self.height]
        return [LineString([up_left, up_right]), LineString([down_left, down_right]),
                LineString([up_left, down_left]), LineString([up_right, down_right])]

    def render(self, output_dir: Path) -> None:
        cv2.imwrite(self.path.as_posix())
