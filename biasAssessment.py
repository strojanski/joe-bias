from text_classification import *
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 


url_embedded = "https://openai-api.meetings.bio/api/openai/embeddings"
url_completion = "https://openai-api.meetings.bio/api/openai/chat/completions"
model = "gpt-3.5-turbo"  # "text-embedding-ada-002" #
# open("gpt4_token", "r").read().strip()
token = "MolDNdTf1iTLl4aWEe1eBgYOtecJ5m"
bias_words = "biasDataset.csv"
democrat_bias_words = "democratBias.csv"
republican_bias_words = "republicanBias.csv"
media = {"cnn.com": -1,
        "cnbc.com": -1,
        "cbsnews.com": 0.2,
        "msnbc.com": -0.2,
        "foxbusiness.com": 1,
        "washingtonpost.com": 1}
lemmatizer = WordNetLemmatizer()
topics = open("topics.txt", "r").read()


class BiasAssesment:
    '''
        - democrats 
        + republicans
    '''

    def __init__(self, article, author, frequencyWeightMultiMax=1, frequencyDemRepSumMax=1, sentimentSumMax=1, susceptibilityMultiMax=1,
                 chatGPTSumMax=1, authorSumMax=1):
        # we multiply these
        self.frequencyWeightMultiMax = frequencyWeightMultiMax
        self.susceptibilityMultiMax = susceptibilityMultiMax

        # we add these
        self.frequencyDemRepSumMax = frequencyDemRepSumMax
        self.sentimentSumMax = sentimentSumMax
        self.chatGPTSumMax = chatGPTSumMax
        self.authorSumMax = authorSumMax

        self.indexMax = (frequencyDemRepSumMax + sentimentSumMax + chatGPTSumMax + authorSumMax)*frequencyWeightMultiMax * susceptibilityMultiMax  # če bodo vrednosti Multi manjše kot 1 se ne pomnoži za računanje indexMax

        self.article = article
        self.author = author

        self.gpt = GPT4(url_completion, token, model)

    def expand_topic(self):
        keys_list = topics.split("\n")
        print(keys_list)
        my_dict = {key: None for key in keys_list}
        print(my_dict.keys())
        for key in my_dict.keys():
            print(key)
            #dict_list = ([str(lemma.name()) for lemma in wordnet.synsets(key).hypernyms(key)])
            synsets = wordnet.synsets(key)
            #dict_list = [str(lemma.name()) for lemma in synsets]
            synset = synsets[0]
            hypernyms = synset.hypernyms()
            dict_list = [str(lemma.name()) for synset in hypernyms for lemma in synset.lemmas()]
            hyponyms = synset.hyponyms()
            dict_list = [str(lemma.name()) for synset in hyponyms for lemma in synset.lemmas()]
            my_dict[key] = dict_list
        print(my_dict)
        return keys_list

    def frequencyWeight(self):
        '''
            Calculates the frequency weight
        '''
        weightsMax1 = 1
        biased_freq = get_biased_words_frequency(self.article, bias_words)
        print(biased_freq*weightsMax1)
        self.expand_topic()
        return(biased_freq*weightsMax1)

    def subjectivityMulti(self):
        weightsMax = 1
        blob = TextBlob(self.article, analyzer=PatternAnalyzer())
        print(blob.sentiment.subjectivity)
        return blob.sentiment.subjectivity

    def authorSum(self):
        weightMax3 = 1
        return media[self.author]*weightMax3

    def frequencyDemRepSum(self):
        '''
            Calculates the frequency weight by coadding negative democrat and positive republican frequency weights
        '''
        weightsMax4 = 1
        biased_freq_demo = get_biased_words_frequency(self.article, democrat_bias_words)
        biased_freq_rep = get_biased_words_frequency(self.article, republican_bias_words)
        print((biased_freq_rep - biased_freq_demo)*weightsMax4)
        return((biased_freq_rep - biased_freq_demo)*weightsMax4)

    def sentimentSum(self):
        pass

    def chatGPTSum(self):
        # TODO - get list of topics, localize paragraphs with the topic, ask gpt to get sentiment on the topic
        # Only choose 1-2 topics 
        for topic in topics:
            paragraph = localize_topic(topic)

        pass

    def localize_topic():
        pass

    def indexCalculating(self):
        '''
            Calculates the political bias index
        '''
        return (self.frequencyDemRepSum() + self.authorSum())*self.frequencyWeight()*self.subjectivityMulti()/self.indexMax
        #return ((self.frequencyDemRepSum() + self.sentimentSum() + self.chatGPTSum())*self.frequencyWeight()*self.susceptibilityMulti())/self.indexMax


with open("sample_article.txt", 'r') as f:
        text = f.read()
a = "cnn.com"
bias_assesment = BiasAssesment(text, a)
print(bias_assesment.indexCalculating())

    