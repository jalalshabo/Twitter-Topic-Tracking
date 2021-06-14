import mysql.connector
import json
from dotenv import dotenv_values

#retrieve config values
config = dotenv_values(".env")

#connect to database
db_connection = mysql.connector.connect(username="root",
                                         password="iamcool360",
                                         host="localhost",
                                         database="twitterdatabase",
                                         charset="utf8mb4")

dbcursor = db_connection.cursor()

if db_connection.is_connected():
    print("sql connected")

#user interaction
choice = input("Please enter from where you would like to retrieve the tweets from. (1 for user, 2 for time-period, 3 for ALL): ")

if choice == "1":
    user_id = input("Please enter the user_id from which you would like to retrieve the tweets: ")
    sql_addon = "WHERE userId=\'" + user_id + "\'"
elif choice == "2":
    date_choice = input("Would you like to retrieve the tweets for a single date or a range of dates? (1 for a single date, 2 for a range): ")
    if date_choice == "1":
        chosen_date = input("Please enter the date in which you would like to retrieve the tweets (YYYY-MM-DD): ")
        sql_addon = "WHERE tweetDate BETWEEN \'" + chosen_date + " 00:00:00\'" + " and \'" + chosen_date + " 23:59:59\'"
    elif date_choice == "2":
        start_time_period = input("Please enter the start date in which you would like to retrieve the tweets(YYYY-MM-DD)   : ")
        end_time_period = input("Please enter  the end date in which you would like to retrieve the tweets(YYYY-MM-DD): ")
        sql_addon = "WHERE tweetDate BETWEEN \'" + start_time_period + "\'" + " and \'" + end_time_period + "\'"
elif choice == "3":
    sql_addon = "WHERE tweetDate BETWEEN '2010-01-01' and '2030-01-01'"


# send the SQL statement and retrieve the corresponding tweet



dbcursor.execute("SELECT tweetText FROM tweets_table " + sql_addon)
data = dbcursor.fetchall()

final_result = [str(i) for i in data]

final_result = [string.replace("(", "") for string in final_result]
final_result = [string.replace(")", "") for string in final_result]
final_result = [string.replace("'", "") for string in final_result]


print(final_result)

# export data to .json file
with open('all.json', 'w') as json_file:
    json.dump(final_result, json_file, indent=2)

print("The retrieved tweets can be found in retrieved_tweets.json.")

