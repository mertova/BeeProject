import json
import unittest
from io import BytesIO

import cv2
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
        credentials = "C:/Users/lmert/PhD/BeeProject/BeeProject/data/credentials_microsoft.json"
        try:
            with open(credentials) as credentials_file:
                credentials = json.load(credentials_file)
                cls.service = MicrosoftAzure(credentials["microsoft_api_key"])
                super(MicrosoftTest, cls).setUpClass()
        except FileNotFoundError:
            print("Credentials file not found")
            exit(1)

    @parameterized.expand([("test_form1", "C:/Users/lmert/PhD/BeeProject/BeeProject-dataset/SIFT_final_31_empty/2016/1.png", "2016-1")])
    def test_microsoft_azure(self, name, path, index):
        file_name = "microsoft_" + name + "_" + index + ".png"
        # given
        img_mat = cv2.imread(path)
        img_file = open(path, "rb")
        self._test_and_render(self.service, img_file, img_mat, file_name)


if __name__ == '__main__':
    unittest.main()
