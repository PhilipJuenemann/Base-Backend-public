import io
import os
import os.path
import requests
import json
import convertapi
from google.cloud import vision
from google.oauth2 import service_account
from google.cloud.vision_v1 import AnnotateImageResponse
from dotenv import load_dotenv, find_dotenv



# loading credentials
def pdf_to_text(content,extension):

    convertapi.api_secret = 'api key'

    result = convertapi.convert('txt', { 'File': content }, from_format = extension)


    result.file.save('output.txt')

    with open('output.txt', 'rb') as f:
        text = f.read()
        text = str(text)
        text = text.replace("\\n\\nRead more on pspdfkit.com\\n", " ")
        os.remove('output.txt')


    return text


def detect_document(content):
    """Detects document features in an image."""

    with io.open(content, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    text = json.loads(AnnotateImageResponse.to_json(response))

    text = text['textAnnotations'][0]['description']

    return text

def file_to_text(content):

    extension = os.path.splitext(content)[1].strip(".")

    print(extension)

    if extension in ['pdf','docx']:
        text = pdf_to_text(content,extension)

    elif extension in ['jpeg','jpg','png']:
        text = detect_document(content)

    return text
