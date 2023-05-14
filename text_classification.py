from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import requests
import nltk
import math

url_embedded = "https://openai-api.meetings.bio/api/openai/embeddings"
url_completion = "https://openai-api.meetings.bio/api/openai/chat/completions"
model = "gpt-3.5-turbo"  # "text-embedding-ada-002" #
# open("gpt4_token", "r").read().strip()
token = "MolDNdTf1iTLl4aWEe1eBgYOtecJ5m"
# bias_words = open("biasDataset.csv", "r").read().split("\n")    zato ker sem posplošil


class GPT4:
    def __init__(self, url, token, model="gpt-3.5-turbo"):
        self.model = model
        self.url = url
        self.token = token

    def post_request(self, prompt, role="user"):

        if model == "gpt-3.5-turbo":
            response = requests.post(
                self.url,
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
        else:
            response = requests.post(
                self.url,
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "model": model,
                    "input": prompt,
                },
            )

        return response

    def print_response(self, response):
        if response.ok:
            if model == "gpt-3.5-turbo":
                print(response.json()["choices"][0]["message"]["content"])
            else:
                print(response.json())
        else:
            print(response)


def preprocess_text(text):
    '''
        Takes in a string of text and returns a list of lemmatized tokens
    '''
    # Remove stopwords
    tokens = word_tokenize(text)
    tokens = re.sub(r'[^\w\s]', '', " ".join(tokens))
    tokens = tokens.split(" ")
    stop_words = stopwords.words('english')
    tokens = [token.lower() for token in tokens if token.lower()
              not in stop_words and len(token) > 0 and token != " "]

    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmatized_tokens)


def get_biased_words_frequency(article, bias_words):
    '''
        Returns a dictionary of biased words and their frequencies
    '''
    with open(bias_words, 'r') as g:
        listBias = g.read()
    tokens = nltk.word_tokenize(article)
    freq_dist = nltk.FreqDist([word for word in tokens if word in listBias])
    freq_dist_all = nltk.FreqDist(tokens)
    frequency = sum(freq_dist.values())/(sum(freq_dist_all.values())*math.sqrt(len(listBias)))
    return frequency


if __name__ == '__main__':
    text = "This is a sample sentence, showing off the stop words filtration."
    print(preprocess_text(text))

    
