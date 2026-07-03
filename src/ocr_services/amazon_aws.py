import boto3

from geometry.vertex import Vertex
from table.annotations import OcrAnnotation


def _process_output(outputs, img_width, img_height):
    identified = []

    # Iterate through detected items in the response
    for item in outputs.get('Blocks', []):
        # Filter for lines or words if desired (also consider 'WORD' if needed)
        if item['BlockType'] in ['WORD']:
            # Extract the text
            text = item.get('Text', '')
            confidence = item.get('Confidence', 0) / 100

            # Extract the bounding box coordinates
            box = item.get('Geometry', {}).get('BoundingBox', {})

            # Convert relative coordinates to absolute coordinates
            abs_width = box.get('Width', 0) * img_width
            abs_height = box.get('Height', 0) * img_height
            abs_left = box.get('Left', 0) * img_width
            abs_top = box.get('Top', 0) * img_height

            # Calculate top-left and bottom-right coordinates
            top_left = Vertex(abs_left, abs_top)
            bottom_right = Vertex(abs_left + abs_width, abs_top + abs_height)

            # Append the extracted resources to the list
            identified.append(OcrAnnotation(top_left, bottom_right, text, confidence))

    return identified


class Aws:
    def __init__(self, amazon_credentials):
        self.client = boto3.client('textract',
                                   aws_access_key_id=amazon_credentials['ACCESS_KEY'],
                                   aws_secret_access_key=amazon_credentials['SECRET_KEY'],
                                   region_name=amazon_credentials['REGION'])

    def detect_document(self, image_stream, img_width, img_height) -> list[OcrAnnotation]:
        image = image_stream.getvalue()
        response = self.client.detect_document_text(Document={'Bytes': bytearray(image)})
        return _process_output(response, img_width, img_height)
