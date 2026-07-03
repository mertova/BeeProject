from geometry.rectangle import Rectangle
from geometry.vertex import Vertex
from table.cell import Cell


class OcrAnnotation(Rectangle):
    text: str
    confidence: float

    def __init__(self, pt1: Vertex, pt2: Vertex, text: str, confidence=None):
        super().__init__(pt1, pt2, text)
        super().calculate_center()
        self.confidence = confidence

    def __str__(self):
        return f"\nAnnotation: {self.text}:{self.confidence}:{self.center} \n"

    def __repr__(self):
        return f"\nAnnotation: {self.text}:{self.confidence}:{self.center} \n"


class CellAnnotation:
    text: str = ""
    confidence: float = None
    cell: str
    img: None

    def __init__(self, cell: str):
        self.cell = cell
        self._confidence_count = 0

    def concatenate_text_confidence(self, text: str, confidence: float):
        self.text += text
        if self.confidence is not None:
            self._confidence_count += 1
            self.confidence += (confidence - self.confidence) / self._confidence_count
        else:
            self.confidence = confidence
            self._confidence_count = 1

    def add_snippet(self, img):
        # todo impossible if cell attribute is not cell but cell id
        self.img = self.cell.crop_image(img)

    def __str__(self):
        return f"{self.cell}: \"{self.text}\" conf: {self.confidence}"

    def to_dict(self):
        return {"cell": self.cell, "text": self.text, "confidence": self.confidence}


def compose_cell_annotations(c: str, ocr_annotations, threshold):
    cell_annotation = CellAnnotation(c)
    if len(ocr_annotations) == 1:
        confidence = ocr_annotations[0].confidence
        if confidence > threshold:
            cell_annotation.concatenate_text_confidence(ocr_annotations[0].text, confidence)
    elif len(ocr_annotations) > 1:
        sorted_cell_annotations = sorted(ocr_annotations, key=lambda a: a.center.x)
        for annotation in sorted_cell_annotations:
            if annotation.confidence > threshold:
                cell_annotation.concatenate_text_confidence(annotation.text, annotation.confidence)
    return cell_annotation


def sort_ocr_annotations(ocr_annotations: list[OcrAnnotation], table) -> dict[str, list[OcrAnnotation]]:
    cell_annotations_dict = {}
    for c in table.get_active_cells():
        cell_annotations = []
        for annotation in ocr_annotations:
            if c.contains_point(annotation.center):
                cell_annotations.append(annotation)
        cell_annotations_dict[c.text] = cell_annotations
    return cell_annotations_dict
