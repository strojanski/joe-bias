from flask import Flask
from political_bias import *
import json
    
medias = [
    "cnn.com",
    "cnbc.com",
    "cbsnews.com",
    "msnbc.com",
    "foxnews.com",
    "washingtonpost.com"
]


app = Flask(__name__)

@app.route("/")
def get_daily(): 
    return(get_articles_relevant())

@app.route("/by_link")
def get_content_by_link():

    # art = political_bias.get_articles_relavant().articles
    # return(political_bias.get_article_content(art[50]["url"], art[50]["media_name"]))
    #return(art[50].update({"content" : political_bias.get_article_content(art[50]["url"], art[50]["media_name"])}))
    return(get_article_content("https://www.cnn.com/2023/05/12/business/airbag-inflator-recall-arc/index.html", "CNN"))
    # for i in range(len(art)):
    #     if (art[i]["title"] == title):
    #         return art[i]


@app.route("/similar/<publisher>")
def get_similar_articles(publisher):

    return get_articles_relevant(publisher)

    #return(political_bias.get_similar_articles("https://www.cnn.com/2023/05/12/business/airbag-inflator-recall-arc/index.html", "CNN"))

if __name__ == '__main__':
    app.run()
