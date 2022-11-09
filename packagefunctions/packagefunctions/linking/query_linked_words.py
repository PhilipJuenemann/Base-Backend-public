import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os
import json
from dotenv import load_dotenv, find_dotenv

# Loading credentials

def query_gbc(query):
    return pd.read_gbq(credentials=credentials,query=query)


def get_linked_words(word):
    query = f"""
    SELECT *
    FROM `lewagon-project-356008.linking.initial_links`
    where string_field_0 ='{word}' or string_field_1 ='{word}'"""
    df = query_gbc(query)
    keywords = []
    for index, row in df.iterrows():
        if row[0] == word:
            keywords.append(row[1])
        else:
            keywords.append(row[0])
    return keywords

def get_linked_words_with_hierarchy(word):
    word = word
    query = f"""SELECT *
    FROM `lewagon-project-356008.linking.initial_linking_with_hierarchy`
    where string_field_1 ='{word}' or string_field_2 ='{word}'"""
    df = query_gbc(query)
    df = df.rename(columns = {'string_field_0':'level_3',"string_field_1":"level_2", "string_field_2":"level_1"})
    final_dict = df.to_dict()
    return final_dict,word

#test
