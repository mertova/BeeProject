import unittest
from pathlib import Path

import cv2

from ocr_services import call_services
from ocr_services.google_vision import GoogleVision
from parameterized import parameterized
from test.test_services.ocr_tests import OcrTest


class GoogleTest(OcrTest):
    service: GoogleVision

    @classmethod
    def setUpClass(cls):
        # load credentials
        credentials = Path("../../resources/credentials/credentials_google.json")
        if credentials.is_file():
            cls.service = GoogleVision(credentials)
            super(GoogleTest, cls).setUpClass()
        else:
            print("Credentials file not found")
            exit(1)

    @parameterized.expand([("test_form1", "C:/Users/lmert/PhD/BeeProject/BeeProject-dataset/SIFT_final_31_empty/2016/1.png", "2016-1")])
    def test_ocr(self, name, path, index):
        # image array to stream
        image = cv2.imread(path)
        file_name = "google_" + name + "_" + index + ".png"
        self._test_and_render(self.service, call_services.get_stream_img(image), image, file_name)


if __name__ == '__main__':
    unittest.main()
