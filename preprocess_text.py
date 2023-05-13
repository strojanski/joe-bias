from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re


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





if __name__ == '__main__':
    text = "This is a sample sentence, showing off the stop words filtration."
    print(preprocess_text(text))
