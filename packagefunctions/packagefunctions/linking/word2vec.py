import gensim.downloader
from gensim.models import KeyedVectors

#main function main2vec at the bottom of the code
# - word2vec(directory) - returns a dictionary of best similar work for the topic

# inport the key words function
def import_keywords(directory):

    with open(directory, 'r') as file:
        words = file.read().replace('\n', '')

        listofkwords = words.split('-')
        listofkwords = listofkwords[1:]

    keys = []
    for x in listofkwords:
        keys.append(x.lower())
    keys

    return keys

#keys = import_keywords('../../text/data/data/Keywords/art1.txt')

#gensim models
#List of models provided by gensim
['fasttext-wiki-news-subwords-300', 'conceptnet-numberbatch-17-06-300', 'word2vec-ruscorpora-300',
'word2vec-google-news-300', 'glove-wiki-gigaword-50', 'glove-wiki-gigaword-100', 'glove-wiki-gigaword-200',
'glove-wiki-gigaword-300', 'glove-twitter-25', 'glove-twitter-50', 'glove-twitter-100', 'glove-twitter-200',
'__testing_word2vec-matrix-synopsis']

#import model
def import_model():



    model_wiki = KeyedVectors.load("./packagefunctions/packagefunctions/gigawiki_model/glove-wiki-gigaword-50.d2v")

    return model_wiki

#model_wiki = import_model('glove-wiki-gigaword-50')



# return list of simliar words
def list_similar_key_words(x, model):
    keywords = x

    simwords = []

    try:
        simwords.append(model.most_similar(positive = x, topn=5))

    except:
        simwords.append(["-"])
    # for word in keywords:
    #     try:
    #         simwords.append(model.most_similar(positive = word, topn=5))

    #     except:
    #         simwords.append(["-"])


    return simwords, keywords


#simwords, keywords = list_similar_key_words(keys, model_wiki)


#function to return similar words from a vector combination of list wiki-similar words
def final_similar_list(simwords, model_wiki, num):

    final_list=[]
    for word in simwords:
        for w in word:
            a = w[0]
            b = w[0]
            c = w[0]
            d = w[0]
            e = w[0]

        v_queen = model_wiki[a]
        v_king = model_wiki[b]
        v_man = model_wiki[c]
        v_man1 = model_wiki[d]
        v_man2 = model_wiki[e]

        v_result = v_queen + v_king + v_man + v_man1 + v_man2

        wikisimilarwords = model_wiki.similar_by_vector(v_result, topn=num)
        listword = []
        for word in wikisimilarwords:
            listword.append(word[0])
        final_list.append(listword)

    return final_list

#final_list = final_similar_list(simwords)


# final list of similar words turn into a dictionary
def final_similar_dict(keywords,final_list):

    dictfinal = dict(zip(keywords,final_list))

    return {keywords:final_list}



#dictfinal = final_similar_list(keywords,final_list)


# Main function of the file - word2vec funs all the above function, pass directory in the function

def word2vec(x,num):

    #keys = import_keywords(directory)
    model_wiki = import_model()
    simwords, keywords = list_similar_key_words(x, model_wiki)
    final_list = final_similar_list(simwords, model_wiki,num)
    dictfinal = final_similar_dict(x,final_list)

    return dictfinal


#print(word2vec('./packagefunctions/packagefunctions/arts1.txt'))
