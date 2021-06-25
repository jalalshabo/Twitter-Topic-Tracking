import time
from flask import Flask, jsonify, request


app = Flask(__name__)

sqlstatement = ''

@app.route('/time')
def get_current_time():
    return {'time': time.time() }


@app.route('/add_sqlstatement', methods=['POST'])
def add_sqlstatement():
    sqldata = request.get_json()
    global sqlstatement

    if sqldata['chosenOption'] == 'Overall':
        sqlstatement = "SELECT tweetText FROM tweets_table WHERE tweetDate BETWEEN \'" + sqldata['buttonMessage1'] + "\'" + " and \'" + sqldata['buttonMessage2'] + "\'" 
    elif sqldata['chosenOption'] == 'User':
        sqlstatement = "SELECT tweetText FROM tweets_table WHERE tweetDate BETWEEN \'" + sqldata['buttonMessage1'] + "\'" + " and \'" + sqldata['buttonMessage2'] + "\' AND WHERE userName =\'"
    elif sqldata['chosenOption'] == 'Location':
        sqlstatement = "SELECT tweetText FROM tweets_table WHERE tweetDate BETWEEN \'" + sqldata['buttonMessage1'] + "\'" + " and \'" + sqldata['buttonMessage2'] + "\' AND WHERE tweetCity =\'"
    return 'Statement sent'

@app.route('/sqlstatement')
def get_sql_statement():
    return {'sqlstatement': sqlstatement}