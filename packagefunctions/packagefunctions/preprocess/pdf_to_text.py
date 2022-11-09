import convertapi
import os.path
import requests
import io
import json


def pdf_to_text(content):

    extension = os.path.splitext(content)[1].strip(".")

    convertapi.api_secret = 'api key'

    result = convertapi.convert('txt', { 'File': content }, from_format = extension)

    result.file.save('output.txt')

    with open('output.txt', 'rb') as f:
        text = f.read()
        text = str(text)
        text = text.replace("\\n\\nRead more on pspdfkit.com\\n", " ")
        os.remove('output.txt')


    return text
