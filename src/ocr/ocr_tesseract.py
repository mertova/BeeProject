from pathlib import Path

import pytesseract
from pytesseract import Output
import cv2

from grid import Grid


def ocr_detect_letters(img):
    h, w = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    return img


def ocr_detect_words(img, debug: bool = False):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if debug:
        cv2.imshow('img', img)
        cv2.waitKey(0)
    return d.keys()


def ocr_detect_text(img, debug: bool = False):
    # Adding custom options
    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(img, config=custom_config)
    if debug:
        cv2.imshow('img', img)
        cv2.waitKey(0)
    return result


def annotate_image(img_grey, grid: Grid, index: int, eps: int, intervals: list, results_path: Path, debug: bool = False):

    print("processing image " + str(index) + "\n")
    crops = []
    j = 0
    for cell in grid.cells:
        if (cell.col_id, cell.row_id) in intervals:
            crop = img_grey[cell.pt1[1] - eps:cell.pt2[1] + eps, cell.pt1[0] - eps:cell.pt2[0] + eps]
            if debug:
                cv2.imwrite(results_path.as_posix() + "/crops/" + str(index) + "_" + str(j) + ".png", crop)
            # ocr_detect_letters(crop, str(index) + "_" + str(j) + ".png")
            text = ocr_detect_text(crop)
            cell.annotate(text)
            j += 1
    return grid
