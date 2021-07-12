
# loading json file
import json

# pyLDAvis to visual gensim output
import pyLDAvis.gensim_models

# for stemming tokenized words
import nltk

# for processing the tweets and removing emojis and other garbage input from tweets
import preprocessor.api as preprocessor

# import spacy for tokenizing strings
import spacy
from spacy.lang.en import English


# Gensim to make model
import gensim
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel


class Lda:
    """
    This class handles all LDA features
    ...

    Attributes
    ----------
    corpus: list
    Methods
    -------
    load_json(raw_data)


    """
    def __init__(self):
        self.corpus = []
        pass

    # load json file into empty list as list of stings function
    # send file location, and empty list to load json into 
    def load_json(self, location, empty_list):
        with open(location) as file:
            empty_list = json.load(file)
        # print("Original Data: ", empty_list)
        return empty_list


    # preprocessing library that removes links, new lines, emojis and more, augments the list sent to the function
    def preprocessed_tweets(self, tweet_list):
        for pos, string in enumerate(tweet_list):
            tweet_list[pos] = preprocessor.clean(string)
        # print("Processed: ", tweet_list)


    # removing more garbage that preprocessing library did not capture, need more efficient method for this
    # augments list sent to function
    def remove_garbage(self, tweet_list):
        bad_list = ['\\n', '\\u200c', ':', '//s', '\\t', '.', '?', '!', ',', '"', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', " ' ", '[', ']', ';']
        for bad in bad_list:
            for pos, string in enumerate(tweet_list):
                tweet_list[pos] = string.replace(bad, ' ')
        # print("Garbage Removal: ", tweet_list)


    # tokenization of sentences into words and making each tweet its own list inside the larger tweet list
    # created a new list of all tweets tokenized
    def tokenize(self, tweet_list):

        # loading english language model
        nlp = spacy.load('en_core_web_sm')

        # creating stopwords list by combining nltk stopwords, spacy stopwords and our custom stopwords
        custom_stopwords = ['amp']
        stop_words = nlp.Defaults.stop_words.union(custom_stopwords, nltk.corpus.stopwords.words("english"))

        all_tokenized_tweets = []
        removed_tokens = []
        for strings in tweet_list:
            spacy_doc = nlp(strings)
            one_tweet_list = []
            for token in spacy_doc:
                if token.lower_ not in stop_words and len(token.text) >= 2:
                    one_tweet_list.append(token.lower_)
                else:
                    removed_tokens.append(token)
            all_tokenized_tweets.append(one_tweet_list)
        # print("Tokenized Tweets: ", all_tokenized_tweets)
        # print("Removed: ", removed_tokens)
        return all_tokenized_tweets

    # stem tokenized words using NLTK Porter Stemmer augments the list sent to the function
    def stem_data(self, tweet_list):
        porter_stemmer = nltk.stem.PorterStemmer()
        for pos_list, lists in enumerate(tweet_list):
            for pos_word, token in enumerate(lists):
                tweet_list[pos_list][pos_word] = porter_stemmer.stem(token)
        # print("Stemmed Tweets: ", tweet_list)


    # Removing empty lists with filter, augments list sent
    def remove_empty(self, tweet_list):
        for pos, lists in enumerate(tweet_list):
            tweet_list[pos] = list(filter(lambda name: name.strip(), lists))
        tweet_list = list(filter(None, tweet_list))
        # print("Gensim Ready : ", tweet_list)
        return tweet_list


    def corpus_vis(self, tweet_list, output_name):
        # create dictionary for words in list
        dictionary = gensim.corpora.Dictionary(tweet_list)
        # match documents words with word dictionary
        corpus = [dictionary.doc2bow(word) for word in tweet_list]
        # print(dictionary)
        # print("corpus: ", corpus)

        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=dictionary,
                                                    # num topics
                                                    num_topics=10,
                                                    # Set to 0 for batch learning, > 1 for online iterative learning
                                                    update_every=1,
                                                    # num documents used fr each training chunk
                                                    chunksize=100,
                                                    # number of passes through corpus
                                                    passes=100)

        # send LDA to pyLDAvis to create visualization
        vis_model = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
        pyLDAvis.save_html(vis_model, f'{output_name}.html')

    def run_ldamodel(self, raw_corpus):
        corpus = raw_corpus
        self.preprocessed_tweets(corpus)
        self.remove_garbage(corpus)
        tokenized_tweets = self.tokenize(corpus)
        self.stem_data(tokenized_tweets)
        gensim_ready = self.remove_empty(tokenized_tweets)
        self.corpus_vis(gensim_ready, "ankittwitter")
        return

    # if __name__ == '__main__':
    #     bare_tweets = []
    #     bare_tweets = load_json('C:/Users/JS/PycharmProjects/pythonProject/stream into database/ankittwitter.json', bare_tweets)
    #     preprocessed_tweets(bare_tweets)
    #     remove_garbage(bare_tweets)
    #     tokenized_tweets = tokenize(bare_tweets)
    #     stem_data(tokenized_tweets)
    #     gensim_ready = remove_empty(tokenized_tweets)
    #     corpus_vis(gensim_ready, "ankittwitter")
        