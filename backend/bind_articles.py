from political_bias import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from main import all_articles

# TODO: dictionary with key = publisher, value = list of articles

medias = [
    "cnn",
    "cnbc",
    "cbsnews",
    "msnbc",
    "foxnews",
    "washingtonpost"
]

res = get_articles_relevant() if all_articles == None else all_articles

class BindArticle:
    def __init__(self, article_title, article_desc: str, article_author):
        self.article_title = article_title
        self.article_desc = article_desc
        self.article_author = article_author
        
        
    def get_same_date_articles(self):
        global res
        relevant = res
        
        res = {}
        
        for i in range(len(relevant)):
            if relevant[i]["media_id"] in medias and "espan" not in relevant[i]["url"] and "arabic" not in relevant[i]["url"]:
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
            if author == self.article_author:
                continue
            res[author] = []
            # Get closest articles
            closest = None
            max_similarity = 0
            
            # For each article by an author check for the closest article
            for article in self.article_dict[author]:
                article_title = preprocess_text(article["title"])
                article_desc = preprocess_text(article["desc"])
                
                # Check cosine score in title
                cosine = self.cosine_similarity(self.article_title + self.article_desc, article_title + article_desc)
                jaccard = self.jaccard_similarity(self.article_title + self.article_desc, article_title + article_desc)
                
                avg = (cosine + jaccard) / 2
                
                # Title big weight
                common_words = self.count_common_words(self.article_title, article_title)
                score += common_words * .1
                if common_words >= 2:
                    print("common words: ", common_words, article_title, "|", self.article_title)
                

                score += avg
                if score > max_similarity:
                    max_similarity = score
                    closest = article
                
                res[author] = closest
        
        return res
        
    def count_common_words(self, a1, a2):
        words1 = set(a1.split(" "))
        words2 = set(a2.split(" "))
        
        return len(words1.intersection(words2))
        
    def cosine_similarity(self, a1, a2):
        # Create a TfidfVectorizer to convert the texts into numerical vectors
        vectorizer = TfidfVectorizer()
        vectorized_text1 = vectorizer.fit_transform([a1])
        vectorized_text2 = vectorizer.transform([a2])

        # Compute the cosine similarity between the vectors
        similarity = cosine_similarity(vectorized_text1, vectorized_text2)
        return similarity
    
    
    def jaccard_similarity(self, a1, a2):
        # Tokenize the texts into sets of words
        words1 = set(a1)
        words2 = set(a2)

        # Compute the Jaccard similarity between the word sets
        similarity = len(words1.intersection(words2)) / len(words1.union(words2))
        return similarity

    #def word_frequency(self, article2):
        
        
def get_similar_articles(article):
    article_description = preprocess_text(article["desc"])
    article_title = preprocess_text(article["title"])
    article_author = article["media_id"]
    
    ba = BindArticle(article_title, article_description, article_author)
    ba.get_same_date_articles()
    res = ba.get_similar_articles()
    return res


if __name__ == "__main__": 
    article = res[1]
    while("espan" in article["url"] or "arabic" in article["url"]):
        article = res[np.random.randint(0, len(res))]

    article_description = preprocess_text(article["desc"])
    article_title = preprocess_text(article["title"])
    article_author = article["media_id"]
    ba = BindArticle(article_title, article_description, article_author)
    ba.get_same_date_articles()
    res = ba.get_similar_articles()

 