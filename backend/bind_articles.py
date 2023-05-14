from political_bias import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# TODO: dictionary with key = publisher, value = list of articles

class BindArticle:
    def __init__(self, article: str):
        self.article = article
        
    def get_same_date_articles(self):
        pass
        
        
    def get_similar_articles(self, articles: dict):
        score = 0.0
        
        res = {}
        
        # For each author 
        for author in articles.keys():
            res[author] = None
            # Get closest articles
            closest = None
            min_dist = np.inf
            
            for article in articles[author]:
                cosine = self.cosine_similarity(article)
                jaccard = self.jaccard_similarity(article)
                
                avg = (cosine + jaccard) / 2
                
                if avg < min_dist:
                    min_dist = avg
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
    # Define two example texts
    text1 = "This is the first text."
    text2 = "This is the second text."

    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)


    ba = BindArticle(text1)
    similarity = ba.jaccard_similarity(text2)
    print(similarity)
