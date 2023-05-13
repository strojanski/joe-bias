from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import requests
import nltk

url_embedded = "https://openai-api.meetings.bio/api/openai/embeddings"
url_completion = "https://openai-api.meetings.bio/api/openai/chat/completions"
model = "gpt-3.5-turbo" #"text-embedding-ada-002" # 
token = "MolDNdTf1iTLl4aWEe1eBgYOtecJ5m"#open("gpt4_token", "r").read().strip()
bias_words = open("biasDataset.csv", "r").read().split("\n")

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
    tokens = [token.lower() for token in tokens if token.lower() not in stop_words and len(token) > 0 and token != " "]

    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens


def get_biased_words_frequency():
    '''
        Returns a dictionary of biased words and their frequencies
    '''
    frequency = nltk.FreqDist()
    max_frequency = max(frequency.values())
    for word in frequency.keys():
        frequency[word] = frequency[word] / max_frequency

    biased_freq = list(filter(lambda word: word in bias_words))    
    
    return frequency, biased_freq

if __name__ == '__main__':
    text = "This is a sample sentence, showing off the stop words filtration."
    print(preprocess_text(text))
