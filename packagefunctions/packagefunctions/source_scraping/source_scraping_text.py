import nltk.data
import string



def source_scraping(keyword, text):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    data = text
    sentences = []
    sentences = (tokenizer.tokenize(data))

    source_info_words = {}


    keyword_info = []
    counter_sentences = 0
    for sentence in sentences:
        for word in sentence.split():
            if len(keyword.split()) == 2:
                if (keyword.split()[0].lower() or keyword.split()[1].lower()) == word.translate(str.maketrans('', '', string.punctuation)).lower():
                    keyword_info.append([f"....{' '.join(sentences[counter_sentences - 1].split()[int(len(sentences[counter_sentences - 1].split())/2):])}", sentences[counter_sentences], f"{' '.join(sentences[counter_sentences + 1].split()[int(len(sentences[counter_sentences + 1].split())/2):])}...."])
                    break
            elif counter_sentences == 0:
                if keyword.lower() == word.translate(str.maketrans('', '', string.punctuation)).lower():
                    keyword_info.append([sentences[counter_sentences], f"{' '.join(sentences[counter_sentences + 1].split()[int(len(sentences[counter_sentences + 1].split())/2):])}...."])
                    break
            elif counter_sentences == len(sentences):
                if keyword.lower() == word.translate(str.maketrans('', '', string.punctuation)).lower():
                    keyword_info.append([f"....{' '.join(sentences[counter_sentences - 1].split()[int(len(sentences[counter_sentences - 1].split())/2):])}", sentences[counter_sentences]])
                    break
            elif keyword.lower() == word.translate(str.maketrans('', '', string.punctuation)).lower():
                keyword_info.append([f"....{' '.join(sentences[counter_sentences - 1].split()[int(len(sentences[counter_sentences - 1].split())/2):])}", sentences[counter_sentences], f"{' '.join(sentences[counter_sentences + 1].split()[int(len(sentences[counter_sentences + 1].split())/2):])}...."])
                break
        counter_sentences += 1
    return keyword_info
