import tweepy
import mysql.connector
import json
import sys
from datetime import datetime


# keys.txt contains keys, reads file and saves each key as appropriate to be used for authentication, more secure method
# needed for future

def authenticate():
    with open("keys.txt", "r") as keys:
        data = keys.readlines()
        ckey, csecret, atoken, asecret = [key.split('\n')[0] for key in data]

    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    print("Keys Stored and Tweepy Authenticated")
    return auth, api


# Connect to MySQL database, your local machine information needs to be inserted here

def connect_database(username="root", password="iamcool360", host="localhost", database="TwitterDatabase", charset="utf8mb4"):
    connection = mysql.connector.connect(username=username,
                                         password=password,
                                         host=host,
                                         database=database,
                                         charset=charset)
    cursor = connection.cursor()
    if connection.is_connected():
        print("MySQL Database Connected")
    return connection, cursor


def stream_tweets(auth, filtertype, stream_location = None, stream_user_id = None):
    global stream_filter_type_location
    global stream_filter_type_follow
    stream_filter_type_location = False
    stream_filter_type_follow = False

    # passing authentication to stream listener
    stream = tweepy.Stream(auth, StreamListener())

    # location bounding box streaming
    if filtertype == "location":
        stream_filter_type_location = True
        stream_location = [-137, 25, -59, 59]
        stream.filter(locations = stream_location)
    # else stream user id
    else:
        stream_filter_type_follow = True
        stream.filter(follow=['add user id'])


class StreamListener(tweepy.StreamListener):
    # found on stackoverflow, cant fully understand has to do with class inheritance and such, figure out later!!!!!
    def __init__(self):
        super().__init__()
        self.max_tweets = 2 #***********SET NUMBER OF TWEETS TO STREAM******************
        self.tweet_count = 0

    def on_status(self, status):
        print(status.text)
        print(status.user.id_str)

    # when error returns status code, if code == 420 exit (error that says we have reached streaming limit)
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

    # when data arrives parse data and loud into json file, print contents and make equal too correct field in sql
    # database
    def on_data(self, raw_data):

        try:
                raw_data = json.loads(raw_data)
                raw_data["created_at"] = datetime.strftime(datetime.strptime(raw_data["created_at"], '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
                print(raw_data)
                tweetId = raw_data["id"]
                tweetText = raw_data["text"]
                tweetReplyid = raw_data["in_reply_to_status_id"]
                userReplyId = raw_data["in_reply_to_user_id"]
                retweetCount = raw_data["retweet_count"]
                favoriteCount = raw_data["favorite_count"]
                tweetDate = raw_data["created_at"]
                userId = raw_data["user"]["id"]
                userName = raw_data["user"]["name"]
                userLocation = raw_data["user"]["location"]
                userfollowersCount = raw_data["user"]["followers_count"]
                if (raw_data["place"] == None):
                    tweetCountry = None
                    tweetCity = None
                else:
                    tweetCountry = raw_data["place"]["country"]
                    tweetCity = raw_data["place"]["full_name"]

                cursor.execute('''INSERT INTO tweets_table
                               (tweetId,
                               userId,
                               tweetText,
                               tweetReplyid,
                               userReplyId,
                               retweetCount,
                               favoriteCount,
                               tweetDate,
                               userName,
                               userLocation,
                               userfollowersCount,
                               tweetCountry,
                               tweetCity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (
                    tweetId,
                    userId,
                    tweetText,
                    tweetReplyid,
                    userReplyId,
                    retweetCount,
                    favoriteCount,
                    tweetDate,
                    userName,
                    userLocation,
                    userfollowersCount,
                    tweetCountry,
                    tweetCity
                ))
                connection.commit()

        finally:
            self.tweet_count += 1
            if (self.tweet_count == self.max_tweets):
                print("\nCompleted Streaming, Exiting")
                return False

if __name__ == '__main__':

    # connection = mysql.connector.connect(username='root',
    #                                      password='',
    #                                      host='localhost',
    #                                      database='twitterdatabase',
    #                                      charset='utf8mb4')
    # cursor = connection.cursor()
    # if connection.is_connected():
    #     print("MySQL Database Connected")
    #
    # # keys.txt contains keys, reads file and saves each key as appropriate to be used for authentication, more secure method
    # # needed for future
    # with open("keys.txt", "r") as keys:
    #     data = keys.readlines()
    #     ckey, csecret, atoken, asecret = [key.split('\n')[0] for key in data]
    #
    # # Authenticate via tweepy but ensure that if wait limit is reached, simply wait until over and continue
    # auth = tweepy.OAuthHandler(ckey, csecret)
    # auth.set_access_token(atoken, asecret)
    # api = tweepy.API(auth, wait_on_rate_limit=True)
    #
    # connect_database()
    # authenticate()
    #
    # auth = tweepy.OAuthHandler(ckey, csecret)
    # auth.set_access_token(atoken, asecret)
    # api = tweepy.API(auth, wait_on_rate_limit=True)
    #
    # # Calling stream class to get streams from tweets within specific location (current boundary around US/Canada)
    # stream = tweepy.Stream(auth, StreamListener())
    #
    # # location bounding box streaming
    # stream_filtertype_location = False
    # # stream.filter(locations=[-137, 25, -59, 59])
    #
    # # user specific streaming
    # stream_filtertype_follow = True
    # stream.filter(follow=['44196397'])

    # connect to database and return connection and mysql cursor
    connection, cursor = connect_database()
    # authenticate via tweepy and return auth and api
    auth, api = authenticate()
    # send request to stream tweets, send location or userid
    stream_tweets(auth, "follow")

    # Once return false, will close connection and exit program

    cursor.close()
    connection.close()
    sys.exit()
