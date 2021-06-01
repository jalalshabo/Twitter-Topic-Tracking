import mysql.connector, json, pprint
from dotenv import dotenv_values

#retrieve config values
config = dotenv_values(".env")

#connect to database
db_connection = mysql.connector.connect(
    user=config["DB_USERNAME"],
    password=config["DB_PASSWORD"],
    host=config["DB_HOST"],
    database=config["DB_NAME"]
)

# select tweet id and text information
mycurse = db_connection.cursor()
mycurse.execute("SELECT tweetId, tweetText FROM tweets_table")
myresult = mycurse.fetchall()

# reformat data to python dict
data = {}
for x in myresult:
    data[x[0]] = x[1]

# export data to .json file
with open('all_tweets.json', 'w') as json_file:
    json.dump(data, json_file)

