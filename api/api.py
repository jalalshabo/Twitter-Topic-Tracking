import logging, os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# Enable logging for gensim - optional
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

import time, sys
from flask import Flask, jsonify, request, send_file
from twitter_converter import TweetFactory
from lda import Lda


app = Flask(__name__)

tweet_factory = TweetFactory()
lda_factory = Lda()

sqlstatement = ''

@app.route('/api/tweets/location', methods=['GET'])
def get_tweets_location():
    # check if city, start_date and end_date arguments are provided in url
    if 'city' not in request.args:
        return {"error": "missing city argument"}
    
    if 'start_date' not in request.args:
        return {"error": "missing start_date argument"}

    if 'end_date' not in request.args:
        return {"error": "missing end_date argument"}
    
    # retrieve tweets for city
    city = request.args['city']
    start_date = request.args['start_date']
    end_date = request.args['end_date']
    results = tweet_factory.tweets_by_location(city, start_date, end_date)

    # retrieve results on sql success
    if type(results) is list:
        # run lda on results from sql
        proceesed_corpus = lda_factory.train_lda(results)
        # lda_factory.visualize_model(lda_factory.corpus)

        # if (os.path.isfile('./output.html')):
        #     return lda_factory.get_output_json()
        # return proceesed_corpus
        response = jsonify(lda_factory.get_topics())
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    # if the results are errors in json format
    return results

@app.route('/api/tweets/user', methods=['GET'])
def get_tweets_user():
    # check if user_id, start_date and end_date arguments are provided in url
    if 'user_name' not in request.args:
        return {"error": "missing user_name argument"}
    
    if 'start_date' not in request.args:
        return {"error": "missing start_date argument"}

    if 'end_date' not in request.args:
        return {"error": "missing end_date argument"}
    
    # retrieve tweets for user
    user_name = request.args['user_name']
    start_date = request.args['start_date']
    end_date = request.args['end_date']
    results = tweet_factory.tweets_by_user(user_name, start_date, end_date)
    # retrieve results on sql success
    if type(results) is list:
        # run lda on results from sql
        proceesed_corpus = lda_factory.train_lda(results)
        #lda_factory.visualize_model(lda_factory.corpus)

        # checks for visualization output file
        # if (os.path.isfile('./output.html')):
        #     return lda_factory.get_output_json()
        # # if visualization fails, return top topics
        # return lda_factory.get_topics()
        response = jsonify(lda_factory.get_topics())
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    # if the results are errors in json format
    return results

@app.route('/api/tweets/single_date', methods=['GET'])
def get_tweets_single():
    # check if date arguments is provided in the url
    if 'date' not in request.args:
        return {"error": "missing date arguement"}
    
    # retrieve tweets from a single day
    date = request.args['date']
    results = tweet_factory.tweets_by_date_range(date, date)

    # retrieve results on sql success
    if type(results) is list:
        # run lda on results from sql
        proceesed_corpus = lda_factory.train_lda(results)
        #json_response = lda_factory.get_topics()
        # lda_factory.visualize_model(lda_factory.corpus)

        # if (os.path.isfile('./output.html')):
        #     return lda_factory.get_output_json()

        response = jsonify(lda_factory.get_topics())
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    # if the results are errors in json format
    return results

@app.route('/api/tweets/date_range', methods=['GET'])
def get_tweets_range():
    # check if start_date and end_date arguments were provided in url
    if 'start_date' not in request.args:
        return {"error": "missing start_date argument"}

    if 'end_date' not in request.args:
        return {"error": "missing end_date argument"}
    
    # retrieve tweets in date range
    start_date = request.args['start_date']
    end_date = request.args['end_date']
    results = tweet_factory.tweets_by_date_range(start_date, end_date)
    
    # retrieve results on sql success
    if type(results) is list:
        # run lda on results from sql
        proceesed_corpus = lda_factory.train_lda(results)
        # lda_factory.visualize_model(lda_factory.corpus)
    
        # if (os.path.isfile('./output.html')):
        #     response = jsonify(lda_factory.get_output_json())
        #     #response.headers.add('Access-Control-Allow-Origin', '*')
        #     return response
        response = jsonify(lda_factory.get_topics())
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    # if the results are errors in json format
    return results


@app.route('/add_sqlstatement', methods=['POST'])
def add_sqlstatement():
    sqldata = request.get_json()
    global sqlstatement

    if sqldata['chosenOption'] == 'Overall':
        sqlstatement = "SELECT tweetText FROM tweets_table WHERE tweetDate BETWEEN \'" + sqldata['buttonMessage1'] + "\'" + " and \'" + sqldata['buttonMessage2'] + "\'" 
    elif sqldata['chosenOption'] == 'User':
        sqlstatement = "SELECT tweetText FROM tweets_table WHERE tweetDate BETWEEN \'" + sqldata['buttonMessage1'] + "\'" + " and \'" + sqldata['buttonMessage2'] + "\' AND WHERE userName =\'" + sqldata['InputFieldValue'] + "\'"
    elif sqldata['chosenOption'] == 'Location':
        sqlstatement = "SELECT tweetText FROM tweets_table WHERE tweetDate BETWEEN \'" + sqldata['buttonMessage1'] + "\'" + " and \'" + sqldata['buttonMessage2'] + "\' AND WHERE tweetCity =\'" + sqldata['InputFieldValue'] + "\'"
    return 'Statement sent'

@app.route('/sqlstatement')
def get_sql_statement():
    return {'sqlstatement': sqlstatement}