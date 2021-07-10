import time
from flask import Flask, jsonify, request
from twitter_converter import TweetFactory


app = Flask(__name__)
DAL = TweetFactory()

sqlstatement = ''

@app.route('/time', methods=['GET'])
def get_current_time():
    # check id start_date and end_date were provided in url
    if 'start_date' not in request.args:
        return {"error": "missing start_date argument"}

    if 'end_date' not in request.args:
        return {"error": "missing end_date argument"}
    
    # retrieve tweets in date range
    start_date = request.args['start_date']
    end_date = request.args['end_date']
    results = DAL.tweets_by_date_range(start_date, end_date)
    data = {}
    for x in results:
        data[x[0]] = x[1]
    return data


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