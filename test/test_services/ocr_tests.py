import unittest
from pathlib import Path

from src.geometry.vertex import Vertex
from ocr_services import call_services
from table.annotations import OcrAnnotation


class OcrTest(unittest.TestCase):
    # change if needed
    debug_path = Path('../results/7/ocr/')

    @classmethod
    def setUpClass(cls):
        cls.debug_path.mkdir(exist_ok=True, parents=True)

    def _test_and_render(self, service, img_stream, img_mat, out_img: str):

        # when
        ocr_annotations = service.detect_document(img_stream)

        # test
        """
        self.assertIsNotNone(ocr_annotations)
        self.assertGreater(len(ocr_annotations), 0)
        for annotation in ocr_annotations:
            print(annotation)
            self.assertEqual(type(annotation), OcrAnnotation)
            self.assertIsNotNone(type(annotation.pt1), Vertex)
            self.assertIsNotNone(type(annotation.pt2), Vertex)
            self.assertIsNotNone(type(annotation.confidence), float)
        """
        # render
        file_path = self.debug_path / out_img
        call_services.render_annotations(file_path.as_posix(), ocr_annotations, img_mat, True)

