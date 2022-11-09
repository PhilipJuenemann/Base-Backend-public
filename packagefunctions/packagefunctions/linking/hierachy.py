import requests
import wikipedia

def get_word_id(keyword):
    API_ENDPOINT = "https://www.wikidata.org/w/api.php"

    query = keyword

    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'en',
        'search': query
    }


    r = requests.get(API_ENDPOINT, params = params)

    try:
        word_id = r.json()['search'][0]["id"]
    except:
        return "not found"

    return word_id

# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

def get_infos(word_id):

    instances = []
    subclasses = []
    parts = []


    endpoint_url = "https://query.wikidata.org/sparql"

    query = "SELECT ?instance_of ?instance_ofLabel ?subclass_of ?subclass_ofLabel ?part_of ?part_ofLabel ?has_use ?has_useLabel WHERE {wd:"+word_id+" wdt:P279 ?subclass_of .     OPTIONAL {wd:"+word_id+" wdt:P31 ?instance_of .}     OPTIONAL {wd:"+word_id+" wdt:P361 ?part_of . OPTIONAL {wd:"+word_id+" wdt:P366 ?has_use . }}       SERVICE wikibase:label { bd:serviceParam wikibase:language 'en'. } }"

    def get_results(endpoint_url, query):
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()


    results = get_results(endpoint_url, query)


    for result in results["results"]["bindings"]:
        try:
          instances.append(result["instance_ofLabel"]["value"])
        except:
          None
        try:
          subclasses.append(result["subclass_ofLabel"]["value"])
        except:
          None
        try:
          parts.append(result["part_ofLabel"]["value"])
        except:
          None


    seen = set()
    seen_add = seen.add
    subclasses = [x for x in subclasses if not (x in seen or seen_add(x))]

    seen = set()
    seen_add = seen.add
    parts = [x for x in parts if not (x in seen or seen_add(x))]

    seen = set()
    seen_add = seen.add
    instances = [x for x in instances if not (x in seen or seen_add(x))]


    return subclasses, instances, parts


def get_linking_higher(word):
    higher = []
    word_id = get_word_id(word)
    if word_id == "not found":
        done = True
        stop = True
        return [], stop, done

    subclasses, instances, parts = get_infos(word_id)
    stop = False
    done = False

    higher.append(parts)

    if (len(subclasses) + len(instances) + len(parts)) == 0:
        done = True
        return [], stop, done

    if len(higher[0]) > 0:
        stop = True
        return higher[0][0], stop, done
    else:
        higher.pop(0)

    if len(higher) < 1:
        higher.append(subclasses)

    if len(higher) < 1:
        higher.append(instances)

    if len(higher) < 1:
        return [], stop, done
    return higher[0][0], stop, done

def get_part_of(word):
    higher = []
    word_id = get_word_id(word)
    subclasses, instances, parts = get_infos(word_id)
    done = False


    higher.append(parts)


    if len(higher[0]) > 0:
        return higher[0][0], done
    else:
        done = True
        return [], done


def get_hierachy(word):
    hierachy = []
    counter = 0
    hierachy.append(word)
    while counter < 3:


        word, stop, done = get_linking_higher(word)

        if done == True:
            return hierachy

        hierachy.append(word)
        word = hierachy[counter+1]
        counter+=1

        if stop == True:
            word, done = get_part_of(word)
            if done == False:
                hierachy.append(word)
            else:
                return hierachy

    return hierachy


def formatting_hierachy(keyword):
    output = get_hierachy(keyword)
    hierachy = []
    counter = len(output)
    counter_up = 0
    for word in list(reversed(output)):
        try:
            if word == hierachy[counter_up]:
                hierachy.pop(counter_up)
        except:
            None
        hierachy.append(word)

        counter = counter - 1
    return hierachy
