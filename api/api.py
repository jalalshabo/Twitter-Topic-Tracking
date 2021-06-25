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
    
    sqlstatement = "SELECT tweetText FROM tweets_table WHERE tweetDate BETWEEN \'" + sqldata['buttonMessage1'] + "\'" + " and \'" + sqldata['buttonMessage2'] + "\'" 
    return 'Statement sent'

@app.route('/sqlstatement')
def get_sql_statement():
    return {'sqlstatement': sqlstatement}