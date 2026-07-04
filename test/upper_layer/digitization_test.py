import json
import os
import time
import unittest
from pathlib import Path

import cv2

from digitize import Digitize
from image_processing.reference import Reference
from table.table import Table

REPO_ROOT = Path(__file__).resolve().parents[2]
LHI_TABLE_JSON = REPO_ROOT / "resources" / "LHI-final" / "table.json"
LHI_REFERENCE_IMG = REPO_ROOT / "resources" / "LHI-final" / "form_contrasted_31.png"
GOOGLE_CREDENTIALS = REPO_ROOT / "resources" / "credentials" / "credentials_google.json"
MICROSOFT_CREDENTIALS = REPO_ROOT / "resources" / "credentials" / "credentials_microsoft.json"
# Author's private working dataset - never shipped with this repo. The tests below that
# use it are local-only integration smoke tests and will always skip on a fresh clone.
PRIVATE_DATASET = Path("C:/Users/lmert/PhD/BeeProject/BeeProject-dataset/SIFT_final_31_empty-no-1998/")


class DigitizeTest(unittest.TestCase):
    intervals = [('F3', 'I35')]

    def test_decode_intervals(self):
        # given: decode_intervals is pure logic and doesn't touch table/reference/credentials
        digitize = Digitize(None, None, self.intervals, 'google', None)

        # when
        actual_indexes = digitize.decode_intervals()

        # then
        expected_indexes = set()
        for i in range(3, 36):
            expected_indexes.add('F' + str(i))
            expected_indexes.add('G' + str(i))
            expected_indexes.add('H' + str(i))
            expected_indexes.add('I' + str(i))
        self.assertSetEqual(expected_indexes, actual_indexes)

    def test_decode_intervals_empty(self):
        digitize = Digitize(None, None, [], 'google', None)
        actual_indexes = digitize.decode_intervals()
        self.assertSetEqual(set(), actual_indexes)

    def test_decode_intervals_none(self):
        digitize = Digitize(None, None, None, 'google', None)
        self.assertRaises(TypeError, digitize.decode_intervals)


@unittest.skipUnless(PRIVATE_DATASET.is_dir(), "author's private local dataset not present")
class DigitizeIntegrationTest(unittest.TestCase):
    """
    Local-only smoke tests against the full-size unpublished dataset used during
    development of the JCDL'24 paper. Not runnable outside the author's machine.
    """

    debug_path = REPO_ROOT / "test" / "results" / "digitize"

    @classmethod
    def setUpClass(cls):
        cls.debug_path.mkdir(exist_ok=True, parents=True)
        with open(LHI_TABLE_JSON, 'r') as data:
            cls.table = Table()
            cls.table.import_json(json.load(data))
        cls.reference = Reference(cv2.imread(LHI_REFERENCE_IMG.as_posix()), 'sift')

    @unittest.skipUnless(GOOGLE_CREDENTIALS.is_file(), "Google credentials not found")
    def test_digitize_2016_1(self):
        intervals = ['H3', 'I3', 'I4']
        scan = PRIVATE_DATASET.parent / "SIFT_final_31_empty" / "2016" / "1.png"
        digit = Digitize(self.table, self.reference, intervals, 'google', GOOGLE_CREDENTIALS,
                         debug_dir=self.debug_path / "2016-1", transform=False)

        result = digit.run(scan, 0)
        self.assertIsNotNone(result)

    @unittest.skipUnless(GOOGLE_CREDENTIALS.is_file(), "Google credentials not found")
    def test_digitize_form1_google(self):
        self._digitize_dataset('google', GOOGLE_CREDENTIALS)

    @unittest.skipUnless(MICROSOFT_CREDENTIALS.is_file(), "Azure credentials not found")
    def test_digitize_form1_microsoft(self):
        self._digitize_dataset('azure', MICROSOFT_CREDENTIALS)

    def _digitize_dataset(self, service, credentials):
        intervals = [('C3', 'K35')]
        digit = Digitize(self.table, self.reference, intervals, service, credentials, debug_dir=None,
                         transform=False)

        times = []
        for folder in os.listdir(PRIVATE_DATASET.as_posix()):
            out_dir = self.debug_path / service
            out_dir.mkdir(exist_ok=True, parents=True)
            json_result_path = out_dir / (folder + f"-results-{service}.json")
            folder_path = PRIVATE_DATASET / folder
            record_json = {}
            with open(json_result_path.as_posix(), "w") as result_file:
                for x in sorted(folder_path.glob('**/*.png')):
                    if x.is_file():
                        scan_id = x.stem
                        t_start = time.time()
                        record_json[scan_id] = digit.run(x, scan_id)
                        times.append(time.time() - t_start)
                json.dump(record_json, result_file, sort_keys=True, indent=4)

        self.assertGreater(len(times), 0)


if __name__ == '__main__':
    unittest.main()
