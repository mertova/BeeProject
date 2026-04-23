from pathlib import Path

import cv2

from image_processing.image import Image
from image_processing.reference import Reference
from ocr_services.call_services import call_services, render_annotations
from src.table.table import Table
from src.table.cell import decode_index
from src.table.annotations import compose_cell_annotations, sort_ocr_annotations


class Digitize:
    eps = 5
    intervals: list[(str, str)]
    credentials: Path
    table: Table
    reference: Reference
    debug_dir: Path | None

    def __init__(self, table: Table, reference: Reference, intervals: list[(str, str)], credentials: Path,
                 debug_dir=None, transform=True):
        self.intervals = intervals
        self.credentials = credentials
        self.table = table
        self.reference = reference
        self.debug_dir = debug_dir
        self.transform = transform

    def run(self, image_path: Path, i):
        # print("Initialize ... ")
        image_grey = cv2.imread(image_path.as_posix(), cv2.IMREAD_GRAYSCALE)
        indexes = self.decode_intervals()
        self.table.activate(indexes)

        # print("Preprocessing image ", index)
        preprocessed = self._preprocessing(image_grey, self.transform)
        # todo clean = self.clean_image(preprocessed)

        if self.debug_dir is not None:
            path = self.debug_dir / "preprocessed"
            path.mkdir(exist_ok=True, parents=True)
            cv2.imwrite((path/f"{i}.jpg").as_posix(), preprocessed)

        # print("Annotating image ", index)
        services_result = call_services(self.credentials, preprocessed)
        if self.debug_dir is not None:
            path = self.debug_dir / "annotated"
            path.mkdir(exist_ok=True, parents=True)
            render_annotations((path/f"{i}.jpg").as_posix(), services_result['google'], preprocessed,
                               with_text=True)

        # print("Postprocessing annotations ...")
        results_json = {}
        for result in services_result:
            results_json[result] = self._postprocessing_to_json(services_result[result], False, 0.75)
        return results_json

    def _postprocessing_to_json(self, ocr_result, is_number: bool, threshold: float):
        sorted_ocr_annotations = sort_ocr_annotations(ocr_result, self.table)
        results = []
        for c, annotations in sorted_ocr_annotations.items():
            cell_annotation = compose_cell_annotations(c, annotations, threshold)
            # cell_annotation.text.replace(",", ".")
            # cell_annotation.text = re.sub('[^\\d.\\-+]', "", cell_annotation.text)
            if is_number:
                try:
                    cell_annotation.text = float(cell_annotation.text)
                except ValueError:
                    cell_annotation.text = 0
            results.append({'cell': c, 'text': cell_annotation.text, 'confidence': cell_annotation.confidence})
        return results

    def _preprocessing(self, img, transform):
        # todo refactor
        if transform:
            img = self.reference.map_img_to_ref(img)

        # Using cv2.erode() method
        self.reference.erode(2)
        self.reference.sharpening()
        scan = Image(img)
        scan.preprocessing(self.reference.get_inverse())
        return scan.get_grey()

    def decode_intervals(self):
        if self.intervals is None:
            raise TypeError("intervals is not defined")
        indexes = set()
        for interval in self.intervals:
            if type(interval) is tuple:
                col1, row1 = decode_index(interval[0])
                col2, row2 = decode_index(interval[1])
                for i in range(col1, col2 + 1):
                    for j in range(row1, row2 + 1):
                        indexes.add(f"{chr(ord('A') + i)}{j}")
            elif type(interval) is str:
                indexes.add(interval)
            else:
                raise TypeError("intervals is not defined properly: " + interval)

        return indexes
