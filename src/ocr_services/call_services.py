import io
import json
from io import BytesIO

import cv2
from PIL import Image as Im
import numpy as np

from ocr_services.google_vision import GoogleVision
from ocr_services.microsoft_azure import MicrosoftAzure


def call_services(credentials, image: np.array) -> dict:
    """
    Call Google Vision and Microsoft Azure services using credentials.
    :param credentials: json file containing credentials.
    :param image: document to be processed.
    :return: dictionaries containing Google Vision and Microsoft Azure OcrAnnotations.
    """

    # load credentials
    with open(credentials, 'r') as f:
        credentials_json = json.load(f)

    result = {}

    google_vision = GoogleVision(credentials)
    result['google'] = google_vision.detect_document(get_stream_img(image))

    """
    image_pil = Im.fromarray(image)
    image_stream = io.BytesIO()
    image_pil.save(image_stream, format='JPEG')

    azure = MicrosoftAzure(credentials_json['microsoft_api_key'])
    result['azure'] = azure.detect_document(image_stream)
    """
    # ToDO AMAZON AWS, Dtrocr ?
    return result


def get_stream_img(img):
    # image array to stream
    image = Im.fromarray(img)
    with BytesIO() as temp_buffer:
        image.save(temp_buffer, format='png')
        image_data = temp_buffer.getvalue()
    return image_data


def render_annotations(image_path: str, ocr_annotations, canvas, with_text=False):
    # todo calls table annotation
    for annotation in ocr_annotations:
        canvas = annotation.render(canvas, with_text)
    cv2.imwrite(image_path, canvas)
    return canvas
