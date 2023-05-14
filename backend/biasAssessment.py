from text_classification import *
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 
from political_bias import *


url_embedded = "https://openai-api.meetings.bio/api/openai/embeddings"
url_completion = "https://openai-api.meetings.bio/api/openai/chat/completions"
model = "gpt-3.5-turbo"  # "text-embedding-ada-002" #
# open("gpt4_token", "r").read().strip()
token = "MolDNdTf1iTLl4aWEe1eBgYOtecJ5m"
bias_words = "biasDataset.csv"
democrat_bias_words = "democratBias.csv"
republican_bias_words = "republicanBias.csv"
media = {"CNN": -1,
        "cnbc.com": -1,
        "CBS News": 0.2,
        "msnbc.com": -0.2,
        "Fox News": 1,
        "washingtonpost.com": 1}
lemmatizer = WordNetLemmatizer()
topics = open("topics.txt", "r").read()


class BiasAssesment:
    '''
        - democrats 
        + republicans
    '''

    def __init__(self, article, author, frequencyWeightMultiMax=100, frequencyDemRepSumMax=10, sentimentSumMax=1, subjectivityMultiMax=100,
                 chatGPTSumMax=1, authorSumMax=100):
        # we multiply these
        self.frequencyWeightMultiMax = frequencyWeightMultiMax
        self.subjectivityMultiMax = subjectivityMultiMax

        # we add these
        self.frequencyDemRepSumMax = frequencyDemRepSumMax
        self.sentimentSumMax = sentimentSumMax
        self.chatGPTSumMax = chatGPTSumMax
        self.authorSumMax = authorSumMax

        self.indexMax = (frequencyDemRepSumMax + chatGPTSumMax + authorSumMax)*frequencyWeightMultiMax*subjectivityMultiMax  # če bodo vrednosti Multi manjše kot 1 se ne pomnoži za računanje indexMax
        




        self.article = article
        self.author = author
        #print(article)
        
        

    def expand_topic(self):
        keys_list = topics.split("\n")
        #print(keys_list)
        my_dict = {key: None for key in keys_list}
        #print(my_dict.keys())
        for key in my_dict.keys():
            #print(key)
            #dict_list = ([str(lemma.name()) for lemma in wordnet.synsets(key).hypernyms(key)])
            synsets = wordnet.synsets(key)
            #dict_list = [str(lemma.name()) for lemma in synsets]
            synset = synsets[0]
            hypernyms = synset.hypernyms()
            dict_list = [str(lemma.name()) for synset in hypernyms for lemma in synset.lemmas()]
            hyponyms = synset.hyponyms()
            dict_list = [str(lemma.name()) for synset in hyponyms for lemma in synset.lemmas()]
            my_dict[key] = dict_list
        #print(my_dict)
        return my_dict

    def frequencyWeight(self):
        '''
            Calculates the frequency weight
        '''
        biased_freq = get_biased_words_frequency(self.article, bias_words)
        print(biased_freq)
        print(biased_freq*self.frequencyWeightMultiMax)
        self.expand_topic() # Ali je to sploh uporabljeno?
        if biased_freq != 0:
            return(biased_freq*self.frequencyWeightMultiMax)
        else:
            return 1

    def subjectivityMulti(self):
        blob = TextBlob(self.article, analyzer=PatternAnalyzer())
        print(blob.sentiment.subjectivity*self.subjectivityMultiMax)
        if blob.sentiment.subjectivity != 0:
            return blob.sentiment.subjectivity*self.subjectivityMultiMax
        else:
            return 1

    def authorSum(self):
        return media[self.author]*self.authorSumMax

    def frequencyDemRepSum(self):
        '''
            Calculates the frequency weight by coadding negative democrat and positive republican frequency weights
        '''
        biased_freq_demo = get_biased_words_frequency(self.article, democrat_bias_words)
        biased_freq_rep = get_biased_words_frequency(self.article, republican_bias_words)
        #print((biased_freq_rep - biased_freq_demo)*self.frequencyDemRepSumMax)
        return((biased_freq_rep - biased_freq_demo)*self.frequencyDemRepSumMax)

    def sentimentSum(self):
        topics_dict = self.expand_topic()
        for topic in topics_dict.keys():
            for topic in enumerate(self.article):
                pos, top = topic
        for topic_val in topics_dict.values():
            for topic_val in enumerate(self.article):
                pos, top = topic_val
        pass

    def chatGPTSum(self)->float:
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = preprocess_text(self.article)
        self.gpt = GPT4(url_completion, token, model)
        res = self.gpt.post_request(f"Return index from -1 to 1, where -1 represents strong left wing and +1 represents strong right wing for the following text, if you cannot decide, put a number around 0: {' '.join(lemmatized_tokens)}")
        response = self.gpt.print_response(res)
        try:
            response = float(response)
        except ValueError:
            response = 0.0
        assert type(response) == float
        return response*self.chatGPTSumMax 


    def localize_topic(topic):
        pass

    def indexCalculating(self):
        '''
            Calculates the political bias index
        '''
        return (self.frequencyDemRepSum() + self.authorSum() + self.chatGPTSum())*self.frequencyWeight()*self.subjectivityMulti()*300/self.indexMax
        #return ((self.frequencyDemRepSum() + self.sentimentSum() + self.chatGPTSum())*self.frequencyWeight()*self.susceptibilityMulti())/self.indexMax


#text = (get_article_content("https://www.cnn.com/2023/05/12/asia/imran-khan-pakistan-court-army-intl-hnk/index.html", "CNN"))
text = '''to u~e this Introduction merely as a starting point from
which to conduct his own study and criticism of what
Marx and ~lan.ists have wrillen.
TilE TIJEORY OF OBJECITVE DEVELOPMENT
The Marxist system has many bmnches. The central
doctrine, however, is the conception which came to be
known as J fistorical Materialism, or the materialist conception of history. The classic formulation of this doctrine is
found in the preface to the Critique of Political Economy
which i\larx published in 1859. There he describes how
he was led to "the conclusion that legal relations as well
as fonns of the state could neither be understood by
themselves, nor explained by the so-called general progress
of the human mind, but that they are rooted in the material conditions of life." Expanding on this statement, he
continued:
Tn tl1e social production of their material life, men enter
into definite relations that arc indispensable and independent
of their wills; these relations of prOduction corre~pond to a
d(·6nite state of tile development of tlleir material forces of
production.
The sum total of these rclalions of production makes up the
economic structure of society-the real foundation on which
arises a legal and political superstructure and to which correspond definite forms of social coosciou~ncss.
The mode of production of material life determines the social,
political aod intellectual life process in general It is not the
consciousness of men that determines their existence, but rather
it is their social exi~tence that determines their consciousness.
At a cert.1in stage of their dc,•t·lopmcnt, the material forces of
production in society come into conflict with the existing relations of production or-what is but a legal expres~ion of the same thing-with the property relations within which they
have been at work before. From forms of dcvelopmt!nt of the
productive forces, these relatious tum into their fetters. Then
begins an epoeh of social revolution. With the chan~e of the
economic foundation, the entire immense superstructure is more or bs rapidly transformed.
e
INTflODUCTION
ron one hold, as \larx docs, on the one hand that men
are conscaous, purposive, and indted inventive, and em the
other hand, that their social lift>, like the proct•sscs of
blind, physical nature, develops independently of their
thoue;ht and ''ill?
Thanks not n little to the influence of Marx, tltis paradox
is tod~t)' u commonplace of social science, which is very
much conct·rned "ith studying what may be calk I objective devdopmt•nt in socidy. Economists interest themselves, for instance, in working out the unintended consequences of the behavior of a number of p<'oplt· buying
and scllinl( in a free market. In such a situation, lach individual as continually making decisions such a~ '' Ia ether
he shall or shall not o£ler his goods and what prices he
shall a)k for tl1cm. Yet the final outcome of the "hi~~ling"
of the market is not planned and very likely not even
foreseen by anyone. So with the other processes of a free,
competitive economy: while on Lhe one hand they are
carried on by inventive, calculating human beings, on the
other hand they arrive at results which no mind has
previously conceived and purposively carried out. 1t is
as if, to use Adam Smith's phrase, these processes were
guided by "an invisible hand."
Not only in economics, but also in other spheres, processes of objective development take place, providin~ a
subject-matter in which the social scientist seeks to discover uniformities or '1aws" of social change and causation.
To accept this general conclusion one need not be a arxist. f\or i~ there anything peculiarly Marxist about its
application to the study of long-run historical development,
although t.farx was concerned less with repelilive and
short-run processes-such as price formation in a free
market-than with the long-run tendencies of economic
development.
What then distinguishes the Marxian theory of objective
development from the notion of objective development in
general? Economic development, according to ~larx, is
subject to certain inexomble laws and must pass through
certain definite stages. Each stage has its distinctive mode
of production, its system by which the means of produc-
INTRODUCTI0"'-1
history he referred to as the "thesis,'' the opposing productive forces which emerge within it .ts the ··antithesis,"
while the nt:w and more productive t•conOm} which results from the union of the two he tcmH?d the "<;ynthesis."
Marxist economic history, therefore, like the progress
of Hegelian tntth, is governed by t11e laws of dialectical
movement. Under t11cse laws the mode of production is a
whole, a real unity, which gradually produces the forces
which will transform it in a sudden catastrophe. The principal motor of development is not thought, but on the
contrary, the "productive forces" of t11e economy.
What did Marx mean by "productive forces?" The
briefest way of putting it is to say that they are the elements of which the mode of production is composed; they
are the parts, it is the whole. In a modem economy, they
would include, for instance, tools, machines, and factories;
the materials and natural resources which enter into production; the work of labor, skilled, unskilled, and tcchnicaJ;
the manner-e.g. the assembly line-in which labor is
used and, in general, the techniques by which '''
a = "cnn.com"
bias_assesment = BiasAssesment(text, a)
