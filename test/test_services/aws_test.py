import json
import unittest
from io import BytesIO
from pathlib import Path

import cv2
from PIL import Image

from ocr_services import call_services
from ocr_services.amazon_aws import Aws

REPO_ROOT = Path(__file__).resolve().parents[2]
CREDENTIALS = REPO_ROOT / "resources" / "credentials" / "credentials-aws.json"
SAMPLE_IMAGE = REPO_ROOT / "test" / "resources" / "form1" / "samples" / "1.png"


def get_stream_img(img):
    # image array to stream
    image_pil = Image.fromarray(img)
    image_stream = BytesIO()
    image_pil.save(image_stream, format='JPEG')
    return image_stream


@unittest.skipUnless(CREDENTIALS.is_file(), f"AWS credentials not found at {CREDENTIALS}")
class AwsTest(unittest.TestCase):
    def setUp(self):
        with open(CREDENTIALS) as credentials_file:
            credentials = json.load(credentials_file)
        self.service = Aws(credentials)

    def test_aws_textract_form1(self):
        # given
        image = cv2.imread(str(SAMPLE_IMAGE))
        image_data = get_stream_img(image)
        img_height, img_width = image.shape[:2]

        # when
        result = self.service.detect_document(image_data, img_width, img_height)

        # test
        self.assertIsNotNone(result)
        debug_path = REPO_ROOT / 'test' / 'results' / 'ocr' / 'aws_annotations'
        debug_path.mkdir(exist_ok=True, parents=True)
        call_services.render_annotations((debug_path / "form1-1.png").as_posix(), result, image, True)
