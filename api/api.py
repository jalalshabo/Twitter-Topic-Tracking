import time
from flask import Flask, jsonify, request
from twitter_converter import TweetFactory


app = Flask(__name__)
tweet_factory = TweetFactory()

sqlstatement = ''

@app.route('/api/tweets/user', methods=['GET'])
def get_tweets_user():
    # check if user_id, start_date and end_date arguments are provided in url
    if 'user_id' not in request.args:
        return {"error": "missing user_id argument"}
    
    if 'start_date' not in request.args:
        return {"error": "missing start_date argument"}

    if 'end_date' not in request.args:
        return {"error": "missing end_date argument"}
    
    # retrieve tweets for user
    user_id = request.args['user_id']
    start_date = request.args['start_date']
    end_date = request.args['end_date']
    results = tweet_factory.tweets_by_user(user_id, start_date, end_date)

    # retrieve results on sql success
    if type(results) is list:
        data = {}
        for x in results:
            data[x[0]] = x[1]
        return data
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
        data = {}
        for x in results:
            data[x[0]] = x[1]
        return data
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
        data = {}
        for x in results:
            data[x[0]] = x[1]
        return data
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