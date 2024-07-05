import unittest
from io import BytesIO
from pathlib import Path

from PIL import Image

from ocr_services.google_vision import GoogleVision

from parameterized import parameterized

from test.test_services.ocr_tests import OcrTest


def get_stream_img(img):
    # image array to stream
    image = Image.fromarray(img)
    with BytesIO() as temp_buffer:
        image.save(temp_buffer, format='png')
        image_data = temp_buffer.getvalue()
    return image_data


class GoogleTest(OcrTest):
    service: GoogleVision

    @classmethod
    def setUpClass(cls):
        # load credentials
        credentials = Path("../../data/credentials_google.json")
        if credentials.is_file():
            cls.service = GoogleVision(credentials)
            super(GoogleTest, cls).setUpClass()
        else:
            print("Credentials file not found")
            exit(1)

    @parameterized.expand([("test_form1", "./scans/Niedersach_examples_10/Sample_Niedersachsen-4-1.png", "2014-1"),
                           ("test_form2", "./scans/Form2-examples-51-png/1977-7.png", "1997-7"),
                           ("test_form1_no_template", "../test/scans/form1_removed_template/2014-1.png", "2014-1-1")])
    def test_ocr(self, name, path, index):
        file_name = "google_" + name + "_" + index + ".png"
        self._test_and_render(self.service, path, file_name)


if __name__ == '__main__':
    unittest.main()
