import requests

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from datetime import datetime, timedelta
import re

import os
import requests
from bs4 import BeautifulSoup

api_key = "5377f7ea28354f08a9ed7a584c086622"


class ArticleRequest:
    def __init__(self, url):
        self.url = url
        self.res = requests.get(url)
        self.article_urls = ""
        self.articles = []

    def get_number_of_articles(self):
        return self.res.json()["totalResults"]

    def get_articles(self):
        #print(requests.get(self.url).json())
        res =  requests.get(self.url).json()
        return res["articles"] if "articles" in res.keys() else []

    def set_url(self, url):
        self.url = url

    def parse_articles(self):
        # list = []
        for article in self.get_articles():
            data = {}
            data.update({'media_id': article["source"]['id']})
            data.update({'media_name': article["source"]['name']})
            data.update({'author': article["author"]})
            data.update({'title': article["title"]})
            data.update({'url': article["url"]})
            data.update({'date': article["publishedAt"]})
            data.update({'desc': article["description"]})
            self.articles.append(data)
            # list.append(data)
        return self.articles


def preprocess_text(text):
    '''
        Takes in a string of text and returns a list of lemmatized tokens
    '''
    # Remove stopwords
    tokens = word_tokenize(text)
    tokens = re.sub(r'[^\w\s]', '', " ".join(tokens))
    tokens = tokens.split(" ")
    stop_words = stopwords.words('english')
    tokens = [token.lower() for token in tokens if token.lower() not in stop_words and len(token) > 0 and token != " "]

    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmatized_tokens)


def concat_domains(domains):
    domains_string = ""
    index = 0
    for name in domains:
        if index > 0:
            domains_string = domains_string + ","
        domains_string = domains_string + name
        index += 1

    return domains_string


# generate url based on time frame:
# date - date of the original article
# num_of_days - how long in the past it should look
# medii - array of strings of media names it should check
def relavant_urls(date, num_of_days, domains, page):
    if (date == None):
        date = datetime.now().date()
    start_day = date - timedelta(days=num_of_days)
    print("start_day", start_day)
    
    relavant = f"https://newsapi.org/v2/everything?domains={domains}&from={start_day}&to={date}&page={page}&apiKey={api_key}"
    return relavant


def extract_content_from_html(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    content = soup.get_text()
    return content

def get_article_content(article_url, article_media_name):
    # request for all the media sources
    article_url_response = requests.get(article_url)
    #print(article_url_response)

    if (article_media_name == "The Washington Post"):
        if article_url_response.ok:
            soup = BeautifulSoup(article_url_response.text, "html.parser")
            content = str(soup.find(class_="grid-body"))
            return(" ".join(extract_content_from_html(content[content.find('drop-cap-letter') + 28:]).split()))

    elif (article_media_name == "CNN"):
        if article_url_response.ok:
            soup = BeautifulSoup(article_url_response.text, "html.parser")
            content = str(soup.find(class_="article__content"))
            return(" ".join(extract_content_from_html(content).split()))

    elif (article_media_name == "CBS News"):
        if article_url_response.ok:
            soup = BeautifulSoup(article_url_response.text, "html.parser")
            content = str(soup.find(class_="content__body"))
            return(" ".join(extract_content_from_html(content[:content.find('chartbeat') - 25]).split()))

    # todo: check media_name on cnbs, msnbc, fox
    elif (article_media_name == "CNBC"):
        if article_url_response.ok:
            soup = BeautifulSoup(article_url_response.text, "html.parser")
            content = str(soup.find(class_="ArticleBody-articleBody"))
            return(" ".join(extract_content_from_html(content[content.find('group') + 10:]).split()))

    elif (article_media_name == "fox"):
        if article_url_response.ok:
            soup = BeautifulSoup(article_url_response.text, "html.parser")
            content = str(soup.find(class_="article-body"))
            return(" ".join(extract_content_from_html(content[content.find('speakable') + 11:]).split()))

    elif (article_media_name == "MSNBC"):
        if article_url_response.ok:
            soup = BeautifulSoup(article_url_response.text, "html.parser")
            content = str(soup.find(class_="showblog-body__content"))
            return(" ".join(extract_content_from_html(content).split()))

def get_articles_top():
    country = "us"
    date = datetime.now().date() - timedelta(days=2)
    start_day = date - timedelta(days=3)
    domains = concat_domains(medii)
    top_articles_url = f"https://newsapi.org/v2/everything?domains={domains}&from={start_day}&to={date}&apiKey={api_key}"
    #top_articles_url = f"https://newsapi.org/v2/everything?domains={domains}&from={start_day}&to={date}&page={1}&apiKey={api_key}"

    # create top heading articles
    top_articles = ArticleRequest(top_articles_url)
    # parse the articles
    top_articles_parsed = top_articles.parse_articles()
    return top_articles

medii = [
        "cnn.com",
        "cnbc.com",
        "cbsnews.com",
        "msnbc.com",
        "foxnews.com",
        "washingtonpost.com"
]

def get_articles_relevant(publisher=None):

     # construct url for relavant data
    
    domains = concat_domains(medii)
    if publisher != None:
        medii.remove(publisher)

    past_lookahead = 2 # how many days in history to search for the articles
    relavant_url = relavant_urls(None, past_lookahead, domains, 1)
        
    # create relavant articles articles - get first page
    relavant_articles = ArticleRequest(relavant_url)
    relavant_articles.parse_articles()

    # iterate through pages of articles and get all of them
    page_index = 1
    while ((page_index) * 100 < relavant_articles.get_number_of_articles()):
        print(page_index * 100, relavant_articles.get_number_of_articles())
        relavant_url = relavant_urls(None, past_lookahead, domains, page_index)
        relavant_articles.set_url(relavant_url)
        relavant_articles.parse_articles()
        page_index += 1
        if page_index * 100 > relavant_articles.get_number_of_articles():
            break
        
    return relavant_articles.articles

# example:
# print(get_articles_relavant().articles[50])
# print(get_article_content(get_articles_relavant().articles[50]["url"], get_articles_relavant().articles[50]["media_name"]))
