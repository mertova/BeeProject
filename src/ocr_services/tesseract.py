import pytesseract
from pytesseract import Output
import cv2

from geometry.vertex import Vertex
from table.annotations import OcrAnnotation


class Tesseract:
    # todo finish by snippets or by whole picture?
    def __init__(self):
        pass


def ocr_detect_words(img):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['char'])
    annotations = []
    for i in range(n_boxes):
        confidence = int(d['conf'][i]) / 100
        if int(d['conf'][i]) > 0.6:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            pt1 = Vertex(x, y)
            pt2 = Vertex(x + w, y + h)
            annotations.append(OcrAnnotation(pt1, pt2, confidence))
    print(d.keys)
    return annotations


def ocr_detect_text(img, debug: bool = False):
    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(img, config=custom_config)
    if debug:
        cv2.imshow('img', img)
        cv2.waitKey(0)
    return result
