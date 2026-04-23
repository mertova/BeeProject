from pathlib import Path
import cv2
import numpy as np
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
    def __init__(self, ref_img, algo):
        """
        The FormAnalysis class is designed to analyze a collection of sample documents and extract a universal, averaged
        empty form image.
        :param ref_img: Reference image for transformation purposes
        :param algo: enable the use of multiple algorithms, SIFT - Scale-invariant feature transform - \"sift\", and ORB
         - Oriented FAST and Rotated BRIEF - \"orb\", allowing the user to specify different algorithms for different
         needs.
        """
        self.reference = Reference(ref_img, algo)

    def extract(self, data_sample_dir: Path | None, limit: int, transform: bool, pen_elimination: bool) -> Reference:
        """
        The main function of the class, extract, detects and extracts standardized forms. It identifies the template
        from the sample dataset and reference image, based on the comon and overlapping pixels.
        :param data_sample_dir: Directory where data samples are stored.
        :param limit: Maximum number of samples used for extraction.
        :param transform: Enable transformation or not.
        :param pen_elimination: Enable averaging or not.
        :return: tuple: recognized template image, average overlapping pixels, and threshold image
        """

        self.reference.pen_elimination()
        if pen_elimination:
            if data_sample_dir is None or not data_sample_dir.exists():
                print("Path does not exist")
                raise SystemExit(1)

            self._averaging(data_sample_dir, limit, transform)
            self.reference.clean_averaged_form()

        return self.reference

    def _averaging(self, data_sample_dir: Path, limit: int, transform: bool):
        print("averaging sample resources ...")
        png_files = data_sample_dir.glob('**/*.png')
        i = 0
        for x in png_files:
            if x.is_file() and i < limit:
                scan = cv2.imread(x.as_posix(), cv2.IMREAD_GRAYSCALE)
                if transform:
                    print("transformed image ", i, ": ", x.name)
                    scan = self.reference.map_img_to_ref(scan)
                self.reference.add_weighted(scan)
                i += 1

