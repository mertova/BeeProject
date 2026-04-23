import json
import os

import sys
import unittest
from pathlib import Path

import cv2

from digitize import Digitize
from image_processing.reference import Reference
from src.table.table import Table
from ocr_services.google_vision import GoogleVision
import time


class DigitizeTest(unittest.TestCase):
    table_form1 = Table
    debug_path = Path("resources/results/14/digitize/")
    # credentials = Path("../resources/credentials_microsoft.json")

    @classmethod
    def setUpClass(cls):
        cls.debug_path.mkdir(exist_ok=True, parents=True)
        """
        with file_form1:
            json_form1 = json.load(file_form1)
            cls.table_form1 = Table()
            cls.table_form1.import_json(json_form1)
            ref_img = cv2.imread(json_form1["template"])
            cls.template = Reference(ref_img)
        """
    def test_decode_intervals(self):
        # given
        intervals = [('F3', 'I35')]
        digitize = Digitize(self.table_form1, self.template, intervals, self.credentials)

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
        # given
        intervals = []
        digitize = Digitize(self.table_form1, self.template, intervals, self.credentials)

        # when
        actual_indexes = digitize.decode_intervals()

        # then
        expected_indexes = set()
        self.assertSetEqual(expected_indexes, actual_indexes)

    def test_decode_intervals_none(self):
        digitize = Digitize(self.table_form1, self.template, None, self.credentials)
        self.assertRaises(TypeError, digitize.decode_intervals)

    def test_digitize_2016_1(self):
        # given
        intervals = ['H3', 'I3', 'I4']

        table_path = Path("../../resources/LHI-final/table.json")
        with open(table_path.as_posix(), 'r') as data:
            table_json = json.load(data)
            table = Table()
            table.import_json(table_json)
            data.close()
        reference_img = cv2.imread("../../resources/LHI-final/form_contrasted_31.png")
        reference = Reference(reference_img)

        credentials = Path("../../resources/credentials/credentials_google.json")

        # test
        scan = Path("C:/Users/lmert/PhD/BeeProject/BeeProject-dataset/SIFT_final_31_empty/2016/1.png")
        digit = Digitize(table, reference, intervals, credentials, debug_dir=Path("resources/results/12/ocr"), transform=False)

        result = digit.run(scan, 0)
        print(result)

    def test_digitize_form1_google(self):
        # given
        intervals = [('C3', 'K35')]
        dataset = Path("C:/Users/lmert/PhD/BeeProject/BeeProject-dataset/SIFT_final_31_empty-no-1998/")
        # dataset = Path("./scans/LHI-transformed-Samples")
        table_path = Path("../../resources/LHI-final/table.json")
        with open(table_path.as_posix(), 'r') as data:
            table_json = json.load(data)
            table = Table()
            table.import_json(table_json)
            data.close()
        reference_img = cv2.imread("../../resources/LHI-final/form_contrasted_31.png")
        reference = Reference(reference_img)

        credentials = Path("../../resources/credentials/credentials_google.json")

        # test
        digit = Digitize(table, reference, intervals, credentials, debug_dir=None,
                         transform=False)

        times = []
        record_json = {}
        for folder in os.listdir(dataset.as_posix()):
            self.debug_path.joinpath("google").mkdir(exist_ok=True, parents=True)
            json_result_path = self.debug_path / "google" / (folder + "-results-google.json")
            folder_path = Path(dataset.as_posix()) / folder
            p = folder_path.glob('**/*.png')
            i = 0
            with open(json_result_path.as_posix(), "w") as result_file:
                for x in p:
                    print(str(i) + " processing scan: " + str(x.name))
                    if x.is_file():
                        scan_id = x.stem
                        t_start = time.time()
                        json_result = digit.run(x, scan_id)
                        elapsed = t_start - time.time()
                        times.append(elapsed)
                        record_json[scan_id] = json_result
                        i += 1
                    else:
                        print("File " + x.name + " is not file")
                json.dump(record_json, result_file, sort_keys=True, indent=4)
                record_json = {}

        print("Time taken: " + str(time.time() - t_start))
        print("Average time: " + str(sum(times) / len(times)))
        print("All times: " + str(times))

    def test_digitize_form1_microsoft(self):
        # given
        intervals = [('C3', 'K35')]
        dataset = Path("C:/Users/lmert/PhD/BeeProject/BeeProject-dataset/SIFT_final_31_empty-no-1998/")
        # dataset = Path("./scans/LHI-transformed-Samples")
        table_path = Path("../../resources/LHI-final/table.json")
        with open(table_path.as_posix(), 'r') as data:
            table_json = json.load(data)
            table = Table()
            table.import_json(table_json)
            data.close()
        reference_img = cv2.imread("../../resources/LHI-final/form_contrasted_31.png")
        reference = Reference(reference_img)

        credentials = Path("../../resources/credentials/credentials_microsoft.json")

        # test
        digit = Digitize(table, reference, intervals, credentials, debug_dir=None,
                         transform=False)

        times = []
        record_json = {}
        for folder in os.listdir(dataset.as_posix()):
            self.debug_path.joinpath("microsoft").mkdir(exist_ok=True, parents=True)
            json_result_path = self.debug_path / "microsoft" / (folder + "-results-microsoft.json")
            folder_path = Path(dataset.as_posix()) / folder
            p = folder_path.glob('**/*.png')
            i = 0
            with open(json_result_path.as_posix(), "w") as result_file:
                for x in p:
                    print(str(i) + " processing scan: " + str(x.name))
                    if x.is_file():
                        scan_id = x.stem
                        t_start = time.time()
                        json_result = digit.run(x, scan_id)
                        elapsed = t_start - time.time()
                        times.append(elapsed)
                        record_json[scan_id] = json_result
                        i += 1
                    else:
                        print("File " + x.name + " is not file")
                json.dump(record_json, result_file, sort_keys=True, indent=4)
                record_json.clear()

        print("Time taken: " + str(time.time() - t_start))
        print("Average time: " + str(sum(times) / len(times)))
        print("All times: " + str(times))


if __name__ == '__main__':
    unittest.main()
    print('Done!')
