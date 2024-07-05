import unittest
from pathlib import Path

import cv2

from src.geometry.vertex import Vertex
from ocr_services import call_services
from table.annotations import OcrAnnotation


class OcrTest(unittest.TestCase):
    # change if needed
    debug_path = Path('../results/7/ocr/')

    @classmethod
    def setUpClass(cls):
        cls.debug_path.mkdir(exist_ok=True, parents=True)

    def _test_and_render(self, service, document_path: str, detected_image: str):
        # given
        img_file = open(document_path, "rb")

        # when
        ocr_annotations = service.detect_document(img_file)

        # test
        self.assertIsNotNone(ocr_annotations)
        self.assertGreater(len(ocr_annotations), 0)
        for annotation in ocr_annotations:
            print(annotation)
            self.assertEqual(type(annotation), OcrAnnotation)
            self.assertIsNotNone(type(annotation.pt1), Vertex)
            self.assertIsNotNone(type(annotation.pt2), Vertex)
            self.assertIsNotNone(type(annotation.confidence), float)
        # render
        file_path = self.debug_path / detected_image
        image = cv2.imread(document_path)
        call_services.render_annotations(file_path.as_posix(), ocr_annotations, image)

