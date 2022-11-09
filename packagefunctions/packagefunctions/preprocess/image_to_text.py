import io
import os
from google.cloud import vision
from google.oauth2 import service_account
import json
from dotenv import load_dotenv, find_dotenv
from google.cloud.vision_v1 import AnnotateImageResponse

# loading credentials
def detect_document(content):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient(credentials = credentials)

    with io.open(content, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    text = json.loads(AnnotateImageResponse.to_json(response))

    text = text['textAnnotations'][0]['description']

    return text
