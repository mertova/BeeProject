from pathlib import Path

import cv2
from shapely import LineString
from pdf2image import convert_from_path


class Template:

    def __init__(self, template_path: Path, template_img=None):
        if template_path is None:
            raise ValueError("Template path does not exist")

        self.path = template_path

        self.template_img = template_img
        self.image_grey = None
        self.height = None
        self.width = None
        self.borders = None

        if template_img is None:
            self.load_img_from_path()

        self.check_colors()
        self.set_template_dimensions()
        self.set_template_borders()

    def check_colors(self):
        if len(self.template_img.shape) == 3:
            self.image_grey = cv2.cvtColor(self.template_img, cv2.COLOR_BGR2GRAY)
        elif len(self.template_img.shape) == 2:
            self.image_grey = self.template_img
        else:
            raise FileNotFoundError("Unsupported file type - image has wrong number of channels")

    def load_img_from_path(self):
        """
        Load image from the template path or the image. Fill in all the parameters of Template class.
        """
        if self.path is None or not self.path.is_file():
            print("directory is not a directory of a file")
            return

        if self.path.suffix.endswith('.pdf'):
            images = convert_from_path(self.path)
            if len(images) != 1:
                raise FileExistsError("pdf file " + self.path.as_posix() + "has several pages. 1 PDF page is "
                                                                           "required.")
            self.image_grey = cv2.cvtColor(images[0], cv2.COLOR_BGR2GRAY)
        elif self.path.suffix.endswith('.jpg') or self.path.suffix.endswith('.png'):
            self.image_grey = cv2.imread(self.path.as_posix(), cv2.IMREAD_GRAYSCALE)
        else:
            raise FileNotFoundError("Unsupported file type")

    def set_template_dimensions(self):
        self.height, self.width = self.image_grey.shape

    def set_template_borders(self):
        """
        creates 4 borderlines from the sape of the image
        :return:
        """
        up_left = [0, 0]
        up_right = [self.width, 0]
        down_left = [0, self.height]
        down_right = [self.width, self.height]
        self.borders = [LineString([up_left, up_right]), LineString([down_left, down_right]),
                        LineString([up_left, down_left]), LineString([up_right, down_right])]

    def dump_template(self):
        cv2.imwrite(self.path.as_posix(), self.image_grey)

    def __str__(self):
        return f"{self.path}"
