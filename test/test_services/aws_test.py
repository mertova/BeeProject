import json
import unittest
from io import BytesIO
from pathlib import Path

import cv2
from PIL import Image

from ocr_services import call_services
from ocr_services.amazon_aws import Aws


def get_stream_img(img):
    # image array to stream
    image_pil = Image.fromarray(img)
    image_stream = BytesIO()
    image_pil.save(image_stream, format='JPEG')
    return image_stream


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # load credentials
        credentials = "../resources/credentials-aws.json"
        try:
            with open(credentials) as credentials_file:
                credentials = json.load(credentials_file)
                self.service = Aws(credentials)
        except FileNotFoundError:
            print("Credentials file not found")
            exit(1)

    def test_google_vision_form1(self):
        # given
        image = cv2.imread("../resources/scans/Niedersach_examples_10/Sample_Niedersachsen-4-1.png")
        image_data = get_stream_img(image)

        # when
        result = self.service.annotate_image(image_data)

        # test
        print(result)
        # test
        debug_path = Path('./results/7/ocr/google_annotations/')
        debug_path.mkdir(exist_ok=True, parents=True)

        call_services.render_annotations(debug_path.as_posix(), result, image, 1)

    def test_google_vision_form2(self):
        # given
        image = cv2.imread("../resources/scans/Form2-examples-51-png/Test 1977-1-15-4_Test 1977-1-15-4-1.png")
        image_data = get_stream_img(image)

        # when
        result = self.service.detect_document(image_data)

        # test
        debug_path = Path('./results/7/ocr/google_annotations/')
        debug_path.mkdir(exist_ok=True, parents=True)

        call_services.render_annotations(debug_path.as_posix(), result, image, 1)
