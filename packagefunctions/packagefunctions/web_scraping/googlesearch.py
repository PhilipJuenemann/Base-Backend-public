import wikipedia
from bs4 import BeautifulSoup
import requests


headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

#fnction to check wiki words otherwise google return
def keyword_summary(word):


    try:
        #wiki search
        title1 = wikipedia.page(word).original_title
        summary1 = wikipedia.summary(word, sentences = 2)
        result = f'{title1} : {summary1}'

    except:
        try:
            #Google - Oxford Dictionary
            html = requests.get(f'https://www.google.com/search?q=what+is+the+definition+of+"{word}', headers=headers)
            soup = BeautifulSoup(html.text, 'html.parser')
            result = f"{word.capitalize()} : {soup.select_one('.LTKOO .sY7ric').text}"

        except:
            result = ("word does not exist")

    return result
