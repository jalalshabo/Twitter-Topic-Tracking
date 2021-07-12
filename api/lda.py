from pprint import pprint

import nltk
nltk.download('stopwords')

import re
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

# logging 
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)




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
        self.raw_corpus = None
        self.processed_corpus = None

        pass

    # preprocessing library that removes links, new lines, emojis and more, augments the list sent to the function
    def preprocess_tweets(self, tweet_corpus):
        return [clean(tweet) for tweet in tweet_corpus]

    
    # run test
    def run_lda(self, tweet_corpus):
        self.raw_corpus = tweet_corpus
        self.processed_corpus = self.preprocess_tweets(tweet_corpus)
        pprint(self.processed_corpus)
        return tweet_corpus

