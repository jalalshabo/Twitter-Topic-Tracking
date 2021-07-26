from os import replace, path
from pprint import pprint
from gensim.corpora import dictionary

import nltk
from nltk import corpus
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')
from nltk.corpus import stopwords

import re, multiprocessing
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as Corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel, Phrases

# preprocess
from preprocessor.api import clean

# spacy for lemmatization
import spacy

# visualization 
import pyLDAvis
import pyLDAvis.gensim_models




class Lda:
    """
        This class uses gensim and the LDA model for topic modelling

        Attributes
        ----------
        stopwords: list
            contains english stop words

        Methods
        -------
        preprocess_tweets(tweet_corpus)
        run_lda(tweet_corpus)
    """
    def __init__(self):
        self.corpus = None                              # collection of documents
        self.trained_model = None                       # trained LDA model
        self.dictionary = None                          # holds frequency counts and extra stats data about the corpus
        self.stopwords = stopwords.words('english')     # commonly used words in the english language
        self.npl = spacy.load('en_core_web_sm')         # more stop words
        self.num_topics = 10                            # number of topics to be extracted
        self.id2word = None                             # mapping from {integer} to word {string}
        self.workers = 4                                # number of extra processes to use for parallel execution
        self.chunksize = 3000                           # how many documents are processed at a time
        self.passes=10                                  # how often we train the model on the entire corpus
        self.batch=True                                 # default value
        self.alpha='symmetric'                          # hyperparameter that affects sparcity of the document-topic (theta) and topic-word (lambda) distributions
        self.eta=None                                   # default value
        self.decay=0.5                                  # default value
        self.offset=1.0                                 # default value
        self.eval_every=None                               # Calculate and log perplexity , None speeds up the algorithm
        self.iterations=400                             # how often we repeat a loop for each document
        self.gamma_threshold=0.001                      # default value
        self.random_state=100                           # default value
        pass


    def print_list(self,_list, msg=''):
        """
        Pretty print a python list
        """
        if type(_list) is list:
            print("{}\n-------------------------".format(msg))
            print(*_list, sep='\n')
    
    # visualize a trained LDA model
    def visualize_model(self, corpus):
        """
        Outputs an html visualization of the trained LDA model 
        """
        output_name = 'output'
        vis_model = pyLDAvis.gensim_models.prepare(self.trained_model, corpus, self.dictionary)
        pyLDAvis.save_html(vis_model, f'{output_name}.html')
        return

    # preprocessing library that removes links, new lines, emojis and more, augments the list sent to the function
    def preprocess_tweets(self, tweet_corpus):
        # clean tweets
        tweets = [ clean(tweet) for tweet in tweet_corpus ]
        # lower each tweet
        tweets = [ tweet.lower() for tweet in tweets]
        # remove extra garbage
        tweets = [re.sub("\'"," ", tweet) for tweet in tweets]
        tweets = [re.sub("[/\^&\*\\\.?!,:\-;\"\[\]]|\\\\n", " ", tweet) for tweet in tweets]
        return tweets

    # Removing empty lists with filter, augments list sent
    def remove_empty(self,tweet_list):
        for pos, lists in enumerate(tweet_list):
            tweet_list[pos] = list(filter(lambda name: name.strip(), lists))
        tweet_list = list(filter(None, tweet_list))
        return tweet_list

    # remove stopwords
    def tokenize(self, tweet_corpus):
        # tokenize the corpus
        tweets = [ tweet.split(" ") for tweet in tweet_corpus]
        # remove numbers but not words that contain numbers
        tweets = [[token for token in tweet if not token.isnumeric()] for tweet in tweets]
        # remove words that only contain one character
        tweets = [[ token for token in tweet if len(token) > 1 ] for tweet in tweets]
        # remove stop words
        custom_stopwords = ['amp', '&amp', '\\c200c', 'u200c', '\\c200d', 'u200d','lol', 'able', 'abst', 'accordance', 'according', 'accodringly', 'act', 'actually',
        'added', 'aint', 'adj', 'affected', 'affecting', 'affects', 'ah', 'all', 'almost', 'announce', 'anybody', 'anymore', 'apparently', 'approximately',
        'arent', 'arise', 'aside', 'ask', 'asking', 'at', 'available', 'away','awful', 'came', 'couldnt', 'cant', 'cause', 'causes', 'certain', 'certainly',
        'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'different', 'dont', 'didnt','downwards', 'ed', 'edu', 'effect', 'end', 'ending', 'especially',
        'et', 'etc', 'everybody', 'ex', 'except', 'far', 'ff', 'fifth', 'fix','followed', 'following', 'follows', 'forth', 'found', 'futhermore',
        'gave', 'gets', 'getting', 'given', 'gives', 'giving', 'goes', 'gone', 'gt', 'got', 'gotten', 'hadnt', 'happens', 'hardly', 'hence', 'id', 'ie', 'ill', 'indeed',
        'instead', 'important', 'importance', 'immediately', 'immediate', 'inc', 'into', 'ive', 'im', 'keeps', 'kept', 'kg', 'km', 'know', 'known', 'knows',
        'largely', 'lest', 'let', 'lets', 'like', 'lately', 'like', 'liked', 'likely', 'look', 'ltd', 'lt', 'maybe', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg',
        'mr', 'mrs', 'na', 'nay', 'near', 'nearly', 'necessary', 'necessarily', 'need', 'needs', 'new', 'ninety', 'non', 'normally', 'nos', 'noted',
        'obtain', 'obtained', 'omg' ,'obviously', 'oh', 'ok', 'okay', 'old', 'outside', 'overall', 'page', 'pages', 'particular', 'particularly', 'placed',
        'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'previously', 'primarily', 'promptly', 'proud', 'provides', 'que', 'quickly', 'quite',
        'regardless', 'regards', 'related', 'right', 'said', 'saw', 'saying', 'sec', 'seeing', 'self', 'several', 'shall', 'shell', 'shouldnt', 'shouldve',
        'showed', 'shown', 'significant', 'significantly', 'similar', 'similarly', 'since', 'slightly', 'soon', 'still', 'sure', 'sup', 'such', 'stop',
        'taken', 'taking', 'tell', 'tends', 'th', 'than','thats', 'thank', 'thanks', 'thatll', 'thatve', 'therell', 'theres', 'theyd', 'theyll', 'theyre', 'theyd', 
        'think', 'this', 'those', 'thru', 'thus', 'til', 'tip', 'took', 'toward', 'towards', 'tried', 'tries', 'try', 'trying', 'twice', 'two', 'un', 'unfortunately',
        'unlike','unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'useful', 'usefully', 'usefulness', 'us', 'using', 'uses', 'usually', 'vis', 'vol',
        'vols', 'vs', 'want', 'wants', 'way', 'wed', 'well', 'whats', 'when', 'whence', 'whos', 'whose', 'widely', 'wouldnt', 'www', 'yall', 'yes', 'youd', 'youll', 'youre',
        'zero', 'z']
        self.stopwords = self.npl.Defaults.stop_words.union(custom_stopwords, self.stopwords)
        return [[token for token in tweet if not token in self.stopwords] for tweet in tweets]
        

    # stem tokenized words using NLTK Porter Stemmer augments the list sent to the function
    def stem_data(self, tweet_corpus):
        porter_stemmer = nltk.stem.PorterStemmer()
        return [[porter_stemmer.stem(token) for token in tweet ]for tweet in tweet_corpus]
    
    # Lemmatize the tokenize word
    def lem_data(self, tweet_corpus):
        lemmatizer = WordNetLemmatizer()
        return [[lemmatizer.lemmatize(token) for token in tweet] for tweet in tweet_corpus ]
    
    def infer_topics(self, unseen_corpus):
        # preprocess new documents
        corpus = self.preprocess_tweets(unseen_corpus)
        corpus = self.tokenize(corpus)
        corpus = self.remove_empty(corpus)
        corpus = self.lem_data(corpus)
        # create dictionary for new corpus
        temp_corpus = [ self.dictionary.doc2bow(document) for document in corpus]
        return self.trained_model[temp_corpus]
    
    # calculate bigrams
    def add_bigrams(self, tweet_corpus):
        corpus = tweet_corpus
        bigrams = Phrases(corpus, min_count=20)
        for idx in range(len(corpus)):
            for token in bigrams[corpus[idx]]:
                if '_' in token:
                    #Token is a bigram and add to corpus
                    corpus[idx].append(token)
        return corpus

    # train new corpus
    def train_lda(self, tweet_corpus):

        # self.print_list(tweet_corpus, "before preprocess")
        # preprocess tweet_corpus 
        corpus = self.preprocess_tweets(tweet_corpus)
        corpus = self.tokenize(corpus)
        corpus = self.remove_empty(corpus)
        corpus = self.lem_data(corpus)
        corpus = self.add_bigrams(corpus)

        #Create a dictionary representation of the documents
        self.dictionary = Corpora.Dictionary(corpus)
        # filter out words that occur in less than 1 document or more than 70% of the corpus
        #self.dictionary.filter_extremes(no_below=2, no_above=0.7)
        # # create a bag-of-words representation of the corpus
        self.corpus = [ self.dictionary.doc2bow(document) for document in corpus]
        ### training the LDA model
        # make a index to word dictionary
        self.dictionary[0] # load the dict to memory
        id_word = self.dictionary.id2token

        # singlecore implementation
        # lda_model = gensim.models.ldamodel.LdaModel(
        #     corpus=self.corpus,
        #     id2word=id_word,
        #     chunksize=self.chunksize,
        #     alpha='auto',
        #     eta='auto',
        #     iterations=self.iterations,
        #     num_topics=self.num_topics,
        #     passes=self.passes,
        #     eval_every=self.eval_every,
        #     update_every=1,
        #     random_state=100,
        #     per_word_topics=True
        # )
        # mulitcore implementation
        self.trained_model = gensim.models.LdaMulticore(
            corpus=self.corpus,
            num_topics=self.num_topics,
            id2word=id_word,
            workers=self.workers,
            chunksize=self.chunksize,
            passes=self.passes,
            batch=self.batch,
            alpha=self.alpha,
            eta=self.eta,
            decay=self.decay,
            offset=self.offset,
            eval_every=self.eval_every,
            iterations=self.iterations,
            gamma_threshold=self.gamma_threshold,
            random_state=self.random_state
        )
        return self.get_topics()

    # get topics
    def get_topics(self):
        """
            Returns a json object in format
            {
                "topic_id": {
                    "word" : "probability",
                },
            }
        """
        # retrieve top 10 words for each topic
        topics = self.trained_model.show_topics(num_topics=self.num_topics, num_words=10, formatted=False)
        # format each topic into json objects
        topics_json_formatted = {}
        for topic in topics:
            words = {}
            for word in topic[1]:
                words[word[0]] = str(word[1])
            topics_json_formatted[topic[0]] = words
            
        return topics_json_formatted
    
    # format output.html and return json version
    def get_output_json(self):
        # read output file

        file = open("output.html", "r")
        data = ""
        for line in file:
            data = data + line
        # extract elements
        link_element = re.search("<link.*>", data).group()
        temp = re.search("<div.*</div>", data)
        div_element = temp.group()
        script_element = data[temp.end() + 1: ]
        # return json
        return_object = {
            "linkElement": link_element,
            "divElement" : div_element,
            "scriptElement" : script_element
        }

        return return_object
