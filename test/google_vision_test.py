import json
import unittest
from io import BytesIO
from pathlib import Path

import cv2
from PIL import Image

from ocr_services import call_services
from ocr_services.google_vision import GoogleVision


def get_stream_img(img):
    # image array to stream
    image = Image.fromarray(img)
    with BytesIO() as temp_buffer:
        image.save(temp_buffer, format='png')
        image_data = temp_buffer.getvalue()
    return image_data


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # load credentials
        credentials = "../data/credentials_google.json"
        self.service = GoogleVision(credentials)

    def test_google_vision_form1(self):
        # given
        image = cv2.imread("./scans/Niedersach_examples_10/Sample_Niedersachsen-4-1.png")
        image_data = get_stream_img(image)

        # when
        result = self.service.detect_document(image_data)

        # test
        print(result)
        self.assertEqual(True, False)

    def test_google_vision_form2(self):
        # given
        image = cv2.imread("./scans/Form2-examples-51-png/Test 1977-1-15-4_Test 1977-1-15-4-1.png")
        image_data = get_stream_img(image)

        # when
        result = self.service.detect_document(image_data)

        # test
        debug_path = Path('./results/7/ocr/google_annotations/')
        debug_path.mkdir(exist_ok=True, parents=True)

        call_services.render_annotations(debug_path.as_posix(), result, image, 1)

    def test_google_vision_without_template(self):
        # given
        image = cv2.imread("../test/results/2/debug_annotation/removed_templates/1.png")
        image_data = get_stream_img(image)

        # when
        annotations = self.service.detect_document(image_data)

        # test
        debug_path = Path('./results/7/ocr/google_annotations/')
        debug_path.mkdir(exist_ok=True, parents=True)

        call_services.render_annotations(debug_path.as_posix(), annotations, image, 1)
        for annotation in annotations:
            print(annotation)


if __name__ == '__main__':
    unittest.main()
