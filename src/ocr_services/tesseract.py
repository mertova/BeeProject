import pytesseract
from pytesseract import Output

from geometry.vertex import Vertex
from table.annotations import OcrAnnotation


class Tesseract:
    """Local OCR engine backed by pytesseract. Requires no credentials."""

    def detect_document(self, image) -> list[OcrAnnotation]:
        data = pytesseract.image_to_data(image, output_type=Output.DICT)
        annotations = []
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            if not text:
                continue
            confidence = int(data['conf'][i]) / 100
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            pt1 = Vertex(x, y)
            pt2 = Vertex(x + w, y + h)
            annotations.append(OcrAnnotation(pt1, pt2, text, confidence))
        return annotations
