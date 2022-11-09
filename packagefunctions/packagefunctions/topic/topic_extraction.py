from google.cloud import language_v1
from google.oauth2 import service_account
import os
import json
from dotenv import load_dotenv, find_dotenv


# loading credentials

def classify(text):
    """Classify the input text into categories."""

    language_client = language_v1.LanguageServiceClient(credentials=credentials)

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={"document": document})
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    return result

def topic_slice(classifier_result):
    """Output: Lowest topic in lowercase"""
    list_topics = list(classifier_result.keys())
    topic_list = []

    for i in list_topics:
        topic_list.append(i.split("/"))

    final_list = []
    for n in topic_list:
        final_list.append(n[-1].lower())

    return final_list
