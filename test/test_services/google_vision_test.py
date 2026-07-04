import unittest
from pathlib import Path

import cv2

from ocr_services import call_services
from ocr_services.google_vision import GoogleVision
from parameterized import parameterized
from test.test_services.ocr_tests import OcrTest

REPO_ROOT = Path(__file__).resolve().parents[2]
CREDENTIALS = REPO_ROOT / "resources" / "credentials" / "credentials_google.json"
SAMPLE_IMAGE = REPO_ROOT / "test" / "resources" / "form1" / "samples" / "1.png"


@unittest.skipUnless(CREDENTIALS.is_file(), f"Google credentials not found at {CREDENTIALS}")
class GoogleTest(OcrTest):
    service: GoogleVision

    @classmethod
    def setUpClass(cls):
        cls.service = GoogleVision(CREDENTIALS)
        super(GoogleTest, cls).setUpClass()

    @parameterized.expand([("test_form1", str(SAMPLE_IMAGE), "form1-1")])
    def test_ocr(self, name, path, index):
        # image array to stream
        image = cv2.imread(path)
        file_name = "google_" + name + "_" + index + ".png"
        self._test_and_render(self.service, call_services.get_stream_img(image), image, file_name)


if __name__ == '__main__':
    unittest.main()
