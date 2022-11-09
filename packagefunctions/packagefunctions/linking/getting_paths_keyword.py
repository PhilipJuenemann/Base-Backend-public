import requests
import pandas as pd
import nltk
import regex as re
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
#nltk.download("omw")
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import numpy as np



def keyword_request(input_text):
    response_keyword = requests.get(
        'https://baseapi-qsjgkov3gq-ew.a.run.app/keyword',
        params={'text': input_text},
    ).json()
    return response_keyword


def topic_request(input_text):
    response_topic = requests.get(
        'https://baseapi-qsjgkov3gq-ew.a.run.app/topic',
        params={'text': input_text},
    ).json()
    return response_topic


def clean_word(text):
    stop_words = set( stopwords.words('english') + list(punctuation) +["''", "»", "''", "‘", "’", '“', '”', '•', '■', '♦️', "'"])
    stemmer = SnowballStemmer("english")
    RE_WSPACE = re.compile(r'\s+', re.IGNORECASE) #find whitespace
    RE_ASCII = re.compile(r'[^A-Za-z0-9\'\/ ]', re.IGNORECASE) #find not alphabet,digits,“,/
    text = re.sub(RE_WSPACE, ' ', text) #convert all whitespaces (tabs etc.) to single wspace
    text = re.sub(RE_ASCII, ' ', text) #delete everything that is not not alphabet,digits,“,/
    text = re.sub('[A-Za-z]+', lambda ele: ' ' + ele[0] + ' ', text)
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    tokens = nltk.word_tokenize(text)
    lemma_function = WordNetLemmatizer()
    lemmas = []
    for token, tag in pos_tag(tokens):
        item = lemma_function.lemmatize(token, tag_map[tag[0]])
        if item not in stop_words:
            lemmas.append(item)
    lemmas=' '.join(lemmas)
    return lemmas

def clean_list(list):
    cleaned_words=[]
    for word in list:
        cleaned_words.append(clean_word(word).lower().replace("'",""))
    return cleaned_words


def hierarchy_request_wikidata(response_keywords):
    list_of_hierarchies=[]
    for word in response_keywords:
        response_hier = requests.get(
        'https://baseapi-qsjgkov3gq-ew.a.run.app/hierachy',
        params={'word': word},
        ).json()
        list_of_hierarchies.append(response_hier)
    return list_of_hierarchies


def wikidata_dict_to_list(wikidata_dict):
    list_of_lists_wikidata=[]
    for x in wikidata_dict:
        list_of_lists_wikidata.append(list(x.values()))
    return list_of_lists_wikidata


def hierarchy_request_google(response_keywords):
    list_of_hierarchies=[]
    for word in response_keywords:
        response = requests.get(
        'https://baseapi-qsjgkov3gq-ew.a.run.app/linkedwords_with_hierarchy',
        params={'word': word},
        )
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204 and response.status_code != 500:
            good_response= response.json()
            list_of_hierarchies.append(good_response)
    return list_of_hierarchies


def google_dict_to_list(google_dict):
    list_of_lists_google =[]
    for word in google_dict:
        list_per_word=[]
        z=list(word[0].values())
        for x in range(len(z)):
            if len(list(z[x].values()))==1:
                list_per_word.append(list(z[x].values())[0])
            else:
                list_per_word.append("")
        list_of_lists_google.append(list_per_word)
    return list_of_lists_google

def google_request_wikidata_hierarchy(hierarchy_list_wikidata):
    #requesting all matches with wikidata from google
    total_hierarchy_request_google=[]
    for word in hierarchy_list_wikidata:
        total_hierarchy_request_google.append(hierarchy_request_google(word))

    #transforming all match dictionaries into lists
    list_of_google_results=[]
    for word in total_hierarchy_request_google:
        list_of_google_results.append(google_dict_to_list(word))

    return list_of_google_results


def extract_keywords_google_and_wikidata(google_wikidata_matches_list):
    google_and_wikidata=[]
    for wikidata_word in google_wikidata_matches_list:
    #print(wikidata_word)
        idx_list=[]
        for index in range(len(wikidata_word)):
            element = [x for x in wikidata_word[index] if x is not None]
            if len("".join(element))!=0:
                idx_list.append(index)
            try:
                idx_true=np.max(idx_list)
                true_ele=wikidata_word[idx_true]
                true_ele = [x for x in true_ele if x is not None]
                condition_one.append(index)
            except:
                true_ele=None
        google_and_wikidata.append(true_ele)
    idx= [x for x in range(len(google_and_wikidata)) if google_and_wikidata[x] is None]
    idx_2= [x for x in range(len(google_and_wikidata)) if google_and_wikidata[x] is not None]
    google_and_wikidata = [x for x in google_and_wikidata if x is not None]

    return google_and_wikidata,idx,idx_2


def extract_keywords_google(hierarchy_list_google,leftover_index_1):
    cases_google =[]
    for index in leftover_index_1:
        if len("".join(hierarchy_list_google[index])) > 0:
            cases_google.append(hierarchy_list_google[index])
            leftover_index_1.remove(index)
    return cases_google,leftover_index_1


def extract_keywords_wikidata(hierarchy_list_wikidata,leftover_index_2):
    cases_wikidata=[]
    for index in leftover_index_2:
        if len(hierarchy_list_wikidata[index])>1:
            cases_wikidata.append(hierarchy_list_wikidata[index])
            leftover_index_2.remove(index)
    return cases_wikidata,leftover_index_2


def extract_keywords_no_match(hierarchy_list_wikidata,leftover_index_3):
    cases_no_match =[]
    for index in leftover_index_3:
        cases_no_match.append(hierarchy_list_wikidata[index])
    return cases_no_match


def get_path_cases_both(cases_both,selected_index):
    final_paths=[]
    for google,index in zip(cases_both,selected_index):
        combined_list = (google + hierarchy_list_wikidata[index])
        seen = set()
        filtered_combined_list=[x for x in combined_list if not (x in seen or seen.add(x))]
        final_paths.append(filtered_combined_list)
    return final_paths


def get_path_cases_wikidata(cases_wikidata,topic):
    final_paths=[]
    for case in cases_wikidata:
        final_paths.append(topic+case)
    return final_paths


def get_path_cases_no_match(cases_no_match,topic):
    final_paths=[]
    for case in cases_no_match:
        final_paths.append(topic+case)
    return final_paths


def get_all_paths(cases_both,selected_index,cases_wikidata,cases_no_match,cases_google,topic):
    all_paths =[]
    for case in get_path_cases_both(cases_both,selected_index):
        all_paths.append(case)
    for case in get_path_cases_wikidata(cases_wikidata,topic):
        all_paths.append(case)
    for case in cases_google:
        all_paths.append(case)
    for case in get_path_cases_no_match(cases_no_match,topic):
        all_paths.append(case)
    return all_paths

# final function

def getting_required_variables(input_text):
    keywords = keyword_request(input_text)
    topic = topic_request(input_text)
    cleaned_keywords = clean_list(keywords)
    hierarchy_wikidata = hierarchy_request_wikidata(cleaned_keywords)
    hierarchy_list_wikidata = wikidata_dict_to_list(hierarchy_wikidata)
    hierarchy_google = hierarchy_request_google(cleaned_keywords)
    hierarchy_list_google = google_dict_to_list(hierarchy_google)
    google_wikidata_matches_list = google_request_wikidata_hierarchy(hierarchy_list_wikidata)
    cases_both,leftover_index_1,selected_index = extract_keywords_google_and_wikidata(google_wikidata_matches_list)
    cases_google,leftover_index_2 = extract_keywords_google(hierarchy_list_google,leftover_index_1)
    cases_wikidata,leftover_index_3=extract_keywords_wikidata(hierarchy_list_wikidata,leftover_index_2)
    cases_no_match = extract_keywords_no_match(hierarchy_list_wikidata,leftover_index_3)
    return cases_both,selected_index,cases_wikidata,cases_no_match,cases_google,topic


def get_paths_from_text(input_text):
    cases_both,selected_index,cases_wikidata,cases_no_match,cases_google,topic = getting_required_variables(input_text)
    return get_all_paths(cases_both,selected_index,cases_wikidata,cases_no_match,cases_google,topic)
