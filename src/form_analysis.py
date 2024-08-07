from pathlib import Path
import cv2
from pdf2image import convert_from_path

from image_processing.reference import Reference


# todo test on .pdf
def load(path: Path = None):
    """
    Load image from the template path or the image. Fill in all the parameters of Template class.
    """
    if path is None or not path.is_file():
        print("path is not a directory of a file")
        exit(1)

    if path.suffix.endswith('.pdf'):
        images = convert_from_path(path)
        if len(images) != 1:
            raise FileExistsError("pdf file " + path.as_posix() + "has several pages. 1 PDF page is "
                                                                  "required.")
        img = images[0]
    elif path.suffix.endswith('.jpg') or path.suffix.endswith('.png'):
        img = cv2.imread(path.as_posix())
    else:
        raise FileNotFoundError("Unsupported file type for reference file")

    return img


class FormAnalysis:
    def __init__(self, out_dir: Path, ref_img):
        self.reference = Reference(ref_img)
        self.out_dir = out_dir

    def extract(self, data_sample_dir: Path | None, limit: int, debug: bool, transform: bool, averaging: bool):
        """
        identify the template from the sample data and reference image based on the comon and overlapping pixels
        :return: tuple: recognized template image, average overlapping pixels, and threshold image
        """

        self.reference.pen_elimination()
        pen_eliminated = self.reference.get_color()

        averaged = None

        if averaging:
            if data_sample_dir is None or not data_sample_dir.exists():
                print("Path does not exist")
                raise SystemExit(1)

            self.averaging(data_sample_dir, limit, transform)
            averaged = self.reference.get_grey()
            self.reference.clean_averaged_form()
        if debug:
            self._dump_debug_images([averaged, pen_eliminated, self.reference.get_grey()])
        else:
            cv2.imwrite((self.out_dir / "mask.png").as_posix(), self.reference.get_color())
        return self.reference.get_grey()

    def averaging(self, data_sample_dir: Path, limit: int, transform: bool):
        print("averaging sample data ...")
        p = data_sample_dir.glob('**/*.png')
        i = 0
        for x in p:
            if x.is_file() and i < limit:
                scan = cv2.imread(x.as_posix(), cv2.IMREAD_GRAYSCALE)
                if transform:
                    print("transformed image ", i, ": ", x.name)
                    scan = self.reference.map_img_to_ref(scan)
                self.reference.add_weighted(scan)
                i += 1
        print("cleaning form ...")

    def _dump_debug_images(self, images):
        debug_dir = self.out_dir / 'debug' / 'templates/'
        debug_dir.mkdir(parents=True, exist_ok=True)
        i = 0
        for img in images:
            if img is not None:
                file_path = debug_dir / Path(str(i) + ".png")
                cv2.imwrite(file_path.as_posix(), img)
            i += 1
