#import openai
import requests

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from datetime import datetime, timedelta
import re

import os
import requests
from bs4 import BeautifulSoup

api_key = "bb5dbc375d1540519dd0b79d4e55c272"

class ArticleRequest:
    def __init__(self, url):
        self.url = url
        self.res = requests.get(url)
        self.article_urls = ""
        self.articles = []
        
    def get_number_of_articles (self):
        return self.res.json()["totalResults"]
    
    def get_articles (self):
        return self.res.json()["articles"]

    def set_url(self, url):
        self.url = url
    
    
    def parse_articles(self):
        list = []
        for article in self.get_articles():
            data = {}
            data.update({'media_id' : article["source"]['id']})
            data.update({'media_name' : article["source"]['name']})
            data.update({'author' : article["author"]})
            data.update({'title' : article["title"]})
            data.update({'url' : article["url"]})
            data.update({'date' : article["publishedAt"]})
            data.update({'desc' : article["description"]})
            list.append(data)
        self.articles.append(list)
        return list

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
    return lemmatized_tokens

def concat_domains (domains):
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
    
    relavant = f"https://newsapi.org/v2/everything?domains={domains}&from={start_day}&to={date}&page={page}&apiKey={api_key}"
    return relavant

def extract_content_from_html(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    content = soup.get_text()
    return content

if __name__ == "__main__":
    country = "us"
    top_articles_url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    # create top heading articles 
    top_articles = ArticleRequest(top_articles_url)
    # parse the articles
    top_articles_parsed = top_articles.parse_articles()
    
    #construct url for relavant data
    medii = [
        "cnn.com",
        "cnbc.com",
        "cbsnews.com",
        "msnbc.com",
        "foxbusiness.com",
        "washingtonpost.com"
    ]
    domains = concat_domains(medii)

    relavant_url = relavant_urls(None, 1, domains, 1)
    # create relavant articles  articles 
    relavant_articles = ArticleRequest(relavant_url)
    page_index = 1
    while (page_index) * 100 < relavant_articles.get_number_of_articles():
        page_index += 1
        print(page_index)
        relavant_url = relavant_urls(None, 1, domains, page_index)
        


    # pages = relavant_articles.get_number_of_articles()
    # for page in range(int(pages / 100) + 1):

    # for article in relavant_articles.articles:
    #     print(article["media_name"])
        # if (article["media_name"] == "The Washington Post"):
        #     article_response = requests.get(article["url"])
        #     if article_response.ok:
        #         soup = BeautifulSoup(article_response.text, "html.parser")
        #         content = str(soup.find(class_="grid-body"))
        #         print("The content is : " + " ".join(extract_content_from_html(content[content.find('drop-cap-letter') + 28:]).split()))

        # elif (article["media_name"] == "CNN"):
        #     article_response = requests.get(article["url"])
        #     if article_response.ok:
        #         soup = BeautifulSoup(article_response.text, "html.parser")
        #         content = str(soup.find(class_="article__content"))
        #         print("The content is : " + " ".join(extract_content_from_html(content).split()))

        # elif (article["media_name"] == "CBS News"):
        #     print(article["url"])
        #     article_response = requests.get(article["url"])
        #     if article_response.ok:
        #         soup = BeautifulSoup(article_response.text, "html.parser")
        #         content = str(soup.find(class_="content__body"))
        #         print("The content is : " + " ".join(extract_content_from_html(content[:content.find('chartbeat') - 25]).split()))

        # todo: check media_name on cnbs, msnbc, fox
        # elif (article["media_name"] == "CNBS"):
        #     article_response = requests.get(article["url"])
        #     if reponse.ok:
        #         soup = BeautifulSoup(reponse.text, "html.parser")
        #         content = str(soup.find(class_="ArticleBody-articleBody"))
        #         print("The content is : " + " ".join(extract_content_from_html(content[content.find('group') + 10:]).split()))

        # elif (article["media_name"] == "fox"):
        #         if reponse.ok:
        #             soup = BeautifulSoup(reponse.text, "html.parser")
        #             content = str(soup.find(class_="article-body"))
        #             print("The content is : " + " ".join(extract_content_from_html(content[content.find('speakable') + 11:]).split()))




