from flask import Flask, jsonify, jsonify
from political_bias import *
from bind_articles import *
    
import json
from flask_cors import CORS
from biasAssessment import *

medias = [
    "cnn.com",
    "cnbc.com",
    "cbsnews.com",
    "msnbc.com",
    "foxnews.com",
    "washingtonpost.com"
]

all_articles = None


app = Flask(__name__)
CORS(app, origins='http://localhost:4200')


def get_bias_from_article(article):
    author = article["media_name"]
    ba = BiasAssesment(article, author)
    return ba.indexCalculating()

@app.route("/")
def get_daily(): 
<<<<<<< HEAD
    print(get_articles_top().articles)
    return jsonify({"titles": get_articles_top().articles})
=======
    titles = get_articles_relevant()
    all_articles = titles
    return jsonify({"titles": titles})
>>>>>>> refs/remotes/origin/master

@app.route("/get_content/<article>")
def get_content_by_link(article):

    # art = political_bias.get_articles_relavant().articles
    # return(political_bias.get_article_content(art[50]["url"], art[50]["media_name"]))
    #return(art[50].update({"content" : political_bias.get_article_content(art[50]["url"], art[50]["media_name"])}))
    return jsonify({"content" : get_article_content(article["url"], article["media_name"])})
    # for i in range(len(art)):
    #     if (art[i]["title"] == title):
    #         return art[i]


@app.route("/similar/<article>")
def get_similar_articles(article):

    return jsonify({"data": get_similar_articles(article)})

    #return(political_bias.get_similar_articles("https://www.cnn.com/2023/05/12/business/airbag-inflator-recall-arc/index.html", "CNN"))

@app.route("/bias/<article>")
def get_bias(article):
    return jsonify({"bias": get_bias_from_article(article["url"], article["media_name"])})


if __name__ == '__main__':
    app.run()
