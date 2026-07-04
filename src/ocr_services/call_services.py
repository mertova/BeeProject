import json
from io import BytesIO

import cv2
from PIL import Image as Im
import numpy as np

from ocr_services.google_vision import GoogleVision
from ocr_services.microsoft_azure import MicrosoftAzure
from ocr_services.amazon_aws import Aws
from ocr_services.tesseract import Tesseract

SERVICES = ('google', 'azure', 'aws', 'tesseract')


def call_services(service: str, credentials, image: np.array) -> dict:
    """
    Run OCR on `image` with the selected service.
    :param service: one of 'google', 'azure', 'aws', 'tesseract'.
    :param credentials: path to the service's credentials .json file (ignored for 'tesseract').
    :param image: document to be processed.
    :return: {service: list[OcrAnnotation]}
    """
    if service not in SERVICES:
        raise ValueError(f"unknown OCR service {service!r}, expected one of {SERVICES}")

    if service == 'google':
        google_vision = GoogleVision(credentials)
        annotations = google_vision.detect_document(get_stream_img(image))
    elif service == 'azure':
        with open(credentials, 'r') as f:
            credentials_json = json.load(f)
        azure = MicrosoftAzure(credentials_json['microsoft_api_key'])
        annotations = azure.detect_document(BytesIO(get_stream_img(image)))
    elif service == 'aws':
        with open(credentials, 'r') as f:
            credentials_json = json.load(f)
        aws = Aws(credentials_json)
        img_height, img_width = image.shape[:2]
        annotations = aws.detect_document(BytesIO(get_stream_img(image)), img_width, img_height)
    else:  # tesseract
        annotations = Tesseract().detect_document(image)

    return {service: annotations}


def get_stream_img(img):
    # image array to stream
    image = Im.fromarray(img)
    with BytesIO() as temp_buffer:
        image.save(temp_buffer, format='png')
        image_data = temp_buffer.getvalue()
    return image_data


def render_annotations(image_path: str, ocr_annotations, canvas, with_text=False):
    for annotation in ocr_annotations:
        canvas = annotation.render(canvas, with_text)
    cv2.imwrite(image_path, canvas)
    return canvas
