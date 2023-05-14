from political_bias import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# TODO: dictionary with key = publisher, value = list of articles

medias = [
    "cnn",
    "cnbc",
    "cbsnews",
    "msnbc",
    "foxnews",
    "washingtonpost"
]


class BindArticle:
    def __init__(self, article: str):
        self.article = article
        
        
    def get_same_date_articles(self):
        relevant = get_articles_relevant()
        
        res = {}
        foreign = ["espanol", "arabic"]
        
        for i in range(len(relevant)):
            if relevant[i]["media_id"] in medias and "espanol" not in relevant[i]["url"] and "arabic" not in relevant[i]["url"]:
                if relevant[i]["media_id"] not in res.keys():
                    res[relevant[i]["media_id"]] = []
                else:
                    res[relevant[i]["media_id"]].append(relevant[i])
                    
        self.article_dict = res
        
        
    def get_similar_articles(self):
        score = 0.0
        
        res = {}
        
        # For each author 
        for author in self.article_dict.keys():
            res[author] = None
            # Get closest articles
            closest = None
            max_similarity = 0
            
            for article in self.article_dict[author]:
                article_meaning = preprocess_text(article["title"] + article["desc"])
                cosine = self.cosine_similarity(article_meaning)
                jaccard = self.jaccard_similarity(article_meaning)
                
                avg = (cosine + jaccard) / 2
                
                if avg > max_similarity:
                    max_similarity = avg
                    closest = article
                
            res[author] = closest
        
        return res
        
        
    def cosine_similarity(self, article2):
        # Create a TfidfVectorizer to convert the texts into numerical vectors
        vectorizer = TfidfVectorizer()
        vectorized_text1 = vectorizer.fit_transform([self.article])
        vectorized_text2 = vectorizer.transform([article2])

        # Compute the cosine similarity between the vectors
        similarity = cosine_similarity(vectorized_text1, vectorized_text2)
        return similarity
    
    
    def jaccard_similarity(self, article2):
        # Tokenize the texts into sets of words
        words1 = set(self.article)
        words2 = set(article2)

        # Compute the Jaccard similarity between the word sets
        similarity = len(words1.intersection(words2)) / len(words1.union(words2))
        return similarity


if __name__ == "__main__": 

    article = get_articles_top().articles[0]
    print(article)
    
    article_description = preprocess_text(article["title"] + article["desc"])
    ba = BindArticle(article_description)
    ba.get_same_date_articles()
    res = ba.get_similar_articles()

    print(res)
