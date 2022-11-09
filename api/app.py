import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import FastAPI, File, UploadFile
#from packagefunctions.keyword import get_keywords_and_nes
from packagefunctions.summary.summary import summary_func
from packagefunctions.summary.summary import preprocess_summary
from packagefunctions.linking.word2vec import word2vec
from packagefunctions.linking.hierachy import formatting_hierachy
from packagefunctions.preprocess.youtube_to_text import youtube_to_text
from packagefunctions.linking.query_linked_words import get_linked_words
from packagefunctions.linking.query_linked_words import get_linked_words_with_hierarchy
from packagefunctions.topic.topic_extraction import classify
from packagefunctions.topic.topic_extraction import topic_slice
from packagefunctions.web_scraping.googlesearch import keyword_summary
from packagefunctions.keywords.keyword_scrape import keyword_preprocessing
from packagefunctions.preprocess.file_to_text import file_to_text
#from packagefunctions.source_scraping import get_five_concepts_keyword
from packagefunctions.linking.getting_paths_keyword import get_paths_from_text
from packagefunctions.source_scraping.source_scraping_text import source_scraping
from packagefunctions.keywords.keyword_gpt3 import preprocessing_keywords

# //for push
#push project


app = FastAPI()

# root `/` endpoint
@app.get("/")
def index():
    return {"ok": True}

@app.get("/youtube")
def youtube(url):
    text = youtube_to_text(url)
    return {'text': text}

@app.post("/upload")
def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()

    try:
        text = file_to_text(tmp_path)
    finally:
        tmp_path.unlink()

    return text

# @app.get("/keyword")
# def keyword(text):
#     response = keyword_func(text)
#     keywords = response
#     final_keywords, list_org, list_person,list_date,list_rest = get_keywords_and_nes(text,keywords)
#     return {'keywords': final_keywords, 'list_org': list_org, 'list_person': list_person, 'list_date': list_date, 'list_rest':list_rest}


@app.get("/keyword")
def keyword(text):
    keywords = preprocessing_keywords(text)
    return keywords

#summary using davinci
@app.get("/summary")
def summary(text, model="text-davinci-002", temperature=0.7, max_tokens=500):
    response = summary_func(text, model=model, temperature=float(temperature), max_tokens=int(max_tokens))
    if len(response) <= 50:
        response1 = summary_func(text, model=model, temperature=float(temperature), max_tokens=int(max_tokens))
        if len(response1) <= 25:
            return "Sorry, summary not possible! Try a different text."
        final_sum = preprocess_summary(response1)
        return final_sum
    else:
        final_sum = preprocess_summary(response)
        return final_sum

@app.get("/word2vecdict")
def word2vecdict(word,num):
    #directory = './text/data/data/Keywords/arts1.txt'
    dictwords = word2vec(word,int(num))
    return dictwords

#matts google search
@app.get("/googlesearch")
def googlesearch(word):
    result = keyword_summary(word)
    return result


@app.get("/hierachy")
def get_word_linking(word):
    return formatting_hierachy(word)

@app.get("/linkedwords")
def get_linked_words_final(word):
    return get_linked_words(word)

@app.get("/linkedwords_with_hierarchy")
def get_linked_words_with_hierarchy_final(word):
    return get_linked_words_with_hierarchy(word)

@app.get("/topic")
def topic_extraction(text):
    classify_output = classify(text)
    return topic_slice(classify_output)

# basic concepts gpt3:
# @app.get("/sourcescraping")
# def five_concepts_keyword_info(keyword):
#     return get_five_concepts_keyword(keyword)

@app.get("/keyword_paths")
def get_paths_keyword(text):
    return get_paths_from_text(text)


@app.get("/keyword_source_info")
def get_sourceinfo_keyword(keyword, text):
    return source_scraping(keyword, text)


@app.get("/full_hierachy")
def get_hierachy(keyword, text):
    hierachy = []
    topic = topic_slice(classify(text))
    keyword_hierachy = formatting_hierachy(keyword)
    for word in topic:
        hierachy.append(word)
    for key in keyword_hierachy:
        hierachy.append(key)
    return hierachy
