import json
import unittest
from io import BytesIO
from PIL import Image as Im

from parameterized import parameterized

from ocr_services.microsoft_azure import MicrosoftAzure
from test.test_services.ocr_tests import OcrTest


def get_stream_img(img):
    # image array to stream
    image = Im.fromarray(img)
    with BytesIO() as temp_buffer:
        image.save(temp_buffer, format='png')
        image_stream = temp_buffer.getvalue()
    return image_stream


class MicrosoftTest(OcrTest):
    service: MicrosoftAzure

    @classmethod
    def setUpClass(cls):
        # load credentials
        credentials = "../data/credentials_microsoft.json"
        try:
            with open(credentials) as credentials_file:
                credentials = json.load(credentials_file)
                cls.service = MicrosoftAzure(credentials["microsoft_api_key"])
                super(MicrosoftTest, cls).setUpClass()
        except FileNotFoundError:
            print("Credentials file not found")
            exit(1)

    @parameterized.expand([("test_form1", "./scans/Niedersach_examples_10/Sample_Niedersachsen-4-1.png", "2014-1"),
                           ("test_form2", "./scans/Form2-examples-51-png/1977-7.png", "1997-7"),
                           ("test_form1_no_template", "../test/scans/form1_removed_template/2014-1.png", "2014-1-1")])
    def test_microsoft_azure(self, name, path, index):
        file_name = "microsoft_" + name + "_" + index + ".png"
        self._test_and_render(self.service, path, file_name)


if __name__ == '__main__':
    unittest.main()
