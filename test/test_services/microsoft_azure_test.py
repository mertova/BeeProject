import json
import unittest
from pathlib import Path

import cv2

from parameterized import parameterized

from ocr_services.microsoft_azure import MicrosoftAzure
from test.test_services.ocr_tests import OcrTest

REPO_ROOT = Path(__file__).resolve().parents[2]
CREDENTIALS = REPO_ROOT / "resources" / "credentials" / "credentials_microsoft.json"
SAMPLE_IMAGE = REPO_ROOT / "test" / "resources" / "form1" / "samples" / "1.png"


@unittest.skipUnless(CREDENTIALS.is_file(), f"Azure credentials not found at {CREDENTIALS}")
class MicrosoftTest(OcrTest):
    service: MicrosoftAzure

    @classmethod
    def setUpClass(cls):
        with open(CREDENTIALS) as credentials_file:
            credentials = json.load(credentials_file)
        cls.service = MicrosoftAzure(credentials["microsoft_api_key"])
        super(MicrosoftTest, cls).setUpClass()

    @parameterized.expand([("test_form1", str(SAMPLE_IMAGE), "form1-1")])
    def test_microsoft_azure(self, name, path, index):
        file_name = "microsoft_" + name + "_" + index + ".png"
        # given
        img_mat = cv2.imread(path)
        with open(path, "rb") as img_file:
            self._test_and_render(self.service, img_file, img_mat, file_name)


if __name__ == '__main__':
    unittest.main()
