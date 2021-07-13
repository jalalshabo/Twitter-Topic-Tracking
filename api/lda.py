from os import replace
from pprint import pprint

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
from gensim.models import CoherenceModel

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
        self.stopwords = None
        self.npl = spacy.load('en_core_web_sm')
        self.corpus = None
        self.processed_corpus = None
        self.num_topics = 10
        self.id2word = None
        self.workers = multiprocessing.cpu_count()
        self.chunksize = 2000
        self.passes=50
        self.batch=True
        self.alpha='symmetric'
        self.eta=None
        self.decay=0.5
        self.offset=1.0
        self.eval_every=None
        self.iterations=50
        self.gamma_threshold=0.001
        self.random_state=100
        pass

    def print_list(self,_list, msg=''):
        if type(_list) is list:
            print("{}\n-------------------------".format(msg))
            print(*_list, sep='\n')

    # preprocessing library that removes links, new lines, emojis and more, augments the list sent to the function
    def preprocess_tweets(self, tweet_corpus):
        # clean tweets
        tweets = [ clean(tweet) for tweet in tweet_corpus ]
        # lower each tweet
        tweets = [ tweet.lower() for tweet in tweets]
        # remove extra garbage
        tweets = [re.sub("\'","", tweet) for tweet in tweets]
        tweets = [re.sub("[\.?!,:-;\"\[\]]|\\\\n", "", tweet) for tweet in tweets]
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
        custom_stopwords = ['amp', '&amp', '\\c200c', '\\c200d']
        self.stopwords = self.npl.Defaults.stop_words.union(custom_stopwords, stopwords.words('english'))
        tweets = [[token for token in tweet if not token in self.stopwords] for tweet in tweets]
        return tweets

    # stem tokenized words using NLTK Porter Stemmer augments the list sent to the function
    def stem_data(self, tweet_corpus):
        porter_stemmer = nltk.stem.PorterStemmer()
        return [[porter_stemmer.stem(token) for token in tweet ]for tweet in tweet_corpus]
    
    # Lemmatize the tokenize word
    def lem_data(self, tweet_corpus):
        lemmatizer = WordNetLemmatizer()
        tweets = [[lemmatizer.lemmatize(token) for token in tweet] for tweet in tweet_corpus ]
        return tweets

    # run test
    def run_lda(self, tweet_corpus):
        corpus = self.preprocess_tweets(tweet_corpus)
        corpus = self.tokenize(corpus)
        corpus = self.remove_empty(corpus)
        corpus = self.lem_data(corpus)

        #Create a dictionary representation of the documents
        dictionary = Corpora.Dictionary(corpus)
        # filter out words that occur in less than 1 document or more than 50% of the corpus
        dictionary.filter_extremes(no_below=2, no_above=0.65)
        # create a bag-of-words representation of the corpus
        self.corpus = [ dictionary.doc2bow(document) for document in corpus]
        ### training the LDA model
        # make a index to word dictionary
        temp = dictionary[0] # load the dict to memory
        id_word = dictionary.id2token

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
        lda_model = gensim.models.LdaMulticore(
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
        output_name = 'output'
        vis_model = pyLDAvis.gensim_models.prepare(lda_model, self.corpus, dictionary)
        pyLDAvis.save_html(vis_model, f'{output_name}.html')

        return tweet_corpus

