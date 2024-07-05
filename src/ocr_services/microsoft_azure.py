import json
import time

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, ComputerVisionOcrErrorException
from msrest.authentication import CognitiveServicesCredentials

from geometry.vertex import Vertex
from table.annotations import OcrAnnotation


def _process_output(response) -> list[OcrAnnotation]:
    annotations = []
    if response.status == OperationStatusCodes.succeeded:
        for text_result in response.analyze_result.read_results:
            for line in text_result.lines:
                for word in line.words:
                    pt1 = Vertex(word.bounding_box[0], word.bounding_box[1])
                    pt2 = Vertex(word.bounding_box[4], word.bounding_box[5])
                    annotations.append(OcrAnnotation(pt1, pt2, word.text, word.confidence))
    return annotations


class MicrosoftAzure:
    def __init__(self, credentials_json: json):
        credentials = CognitiveServicesCredentials(credentials_json['SUBSCRIPTION_KEY'])
        endpoint = credentials_json['ENDPOINT']
        # Authenticate with Azure Cognitive Services.
        self.client = ComputerVisionClient(endpoint=endpoint, credentials=credentials)

    def detect_document(self, image_stream):
        # image_stream.seek(0)  # Rewind the stream to the beginning
        try:
            http_response = self.client.read_in_stream(image_stream, language='en', raw=True)
        except ComputerVisionOcrErrorException as e:
            print(f'AzureVision error: {e.error}')
            # TODO # try lower DPI
            return []

        # Get the operation location (URL with ID as last appendage)
        read_operation_location = http_response.headers["Operation-Location"]

        # Take the ID off and use to get results
        operation_id = read_operation_location.split("/")[-1]

        # Call the "GET" API and wait for the retrieval of the results.
        result = self.client.get_read_result(operation_id)
        while result.status != OperationStatusCodes.succeeded and result.status != OperationStatusCodes.failed:
            time.sleep(1)  # To avoid making too many requests in a short time
            result = self.client.get_read_result(operation_id)
        return _process_output(result)


