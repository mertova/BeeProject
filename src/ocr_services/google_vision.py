from google.cloud import vision_v1
from google.oauth2 import service_account

from geometry.vertex import Vertex
from src.table.annotations import OcrAnnotation


def _process_output(response) -> list[OcrAnnotation]:
    annotations = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        pt1 = Vertex(symbol.bounding_box.vertices[0].x, symbol.bounding_box.vertices[0].y)
                        pt2 = Vertex(symbol.bounding_box.vertices[2].x, symbol.bounding_box.vertices[2].y)
                        annotations.append(OcrAnnotation(pt1, pt2, symbol.text, symbol.confidence))
    return annotations


class GoogleVision:
    def __init__(self, key_path):
        # Authenticate with Google Cloud using the key file
        credentials = service_account.Credentials.from_service_account_file(key_path)
        self.client = vision_v1.ImageAnnotatorClient(credentials=credentials)

    def detect_document(self, image_data):
        """Detects document features in an image."""
        image_context = vision_v1.ImageContext()
        vision_image = vision_v1.Image(content=image_data)
        response = self.client.document_text_detection(image=vision_image, image_context=image_context)
        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )
        return _process_output(response)
