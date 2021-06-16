import tweepy
import mysql.connector
import json
from datetime import datetime


# keys.txt contains keys, reads file and saves each key as appropriate to be used for authentication, more secure method
# needed for future
from tweepy import RateLimitError

# authenticate tweepy using keys text in local folder
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
def connect_database(username="root", password="add passwrod here", host="localhost", database="TwitterDatabase", charset="utf8mb4"):
    connection = mysql.connector.connect(username=username,
                                         password=password,
                                         host=host,
                                         database=database,
                                         charset=charset)
    cursor = connection.cursor()
    if connection.is_connected():
        print("MySQL Database Connected")
    return connection, cursor


# send auth, filter type = location or stream_user_id and will stream based on that
def stream_tweets_location(auth, stream_location):
    global stream_filter_type_location
    stream_filter_type_location = True

    # passing authentication to stream listener
    stream = tweepy.Stream(auth, StreamListener(), tweet_mode="extended")

    # location bounding box streaming
    stream.filter(locations=stream_location)


def stream_tweets_user(auth, stream_user_id):
    global stream_filter_type_follow
    stream_filter_type_follow = True

    # passing authentication to stream listener
    stream = tweepy.Stream(auth, StreamListener(), tweet_mode="extended")

    #setting user id of follow
    stream.filter(follow=[stream_user_id])



class StreamListener(tweepy.StreamListener):
    # found on stackoverflow, cant fully understand has to do with class inheritance and such, figure out later!!!!!
    def __init__(self):
        super().__init__()
        self.max_tweets = stream_max_tweets
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
                print(raw_data)
                raw_data["created_at"] = datetime.strftime(datetime.strptime(raw_data["created_at"], '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
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


# send api and user_id of user to pull specific amounts of tweet from their timeline
# YOU MUST INCLUDE A @ FOR USERNAMES AT THE START
def get_timeline_user(user_id, api, number_of_tweets=3200):
    tweet_count = 0
    timeline_tweets = api.user_timeline(screen_name='user_id', tweet_mode="extended", count="200")
    while tweet_count != number_of_tweets:
        for pos, tweets in enumerate(timeline_tweets):
            tweet_count += 1
            print(tweets._json)
            tweets._json["created_at"] = datetime.strftime(
                datetime.strptime(tweets._json["created_at"], '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
            tweetId = tweets._json["id"]
            tweetText = tweets._json["full_text"]
            tweetReplyid = tweets._json["in_reply_to_status_id"]
            userReplyId = tweets._json["in_reply_to_user_id"]
            retweetCount = tweets._json["retweet_count"]
            favoriteCount = tweets._json["favorite_count"]
            tweetDate = tweets._json["created_at"]
            userId = tweets._json["user"]["id"]
            userName = tweets._json["user"]["name"]
            userLocation = tweets._json["user"]["location"]
            userfollowersCount = tweets._json["user"]["followers_count"]
            if (tweets._json["place"] == None):
                tweetCountry = None
                tweetCity = None
            else:
                tweetCountry = tweets._json["place"]["country"]
                tweetCity = tweets._json["place"]["full_name"]

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
                                                          tweetCity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (
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

            if tweet_count == number_of_tweets:
                return
            elif pos == len(timeline_tweets) - 1:
                oldest = tweets._json["id"]
        # after all 200 tweets pulled will make another request for the next 200 starting from the end of the last tweet
        # thus keep going backwards until total tweet until number_of_tweets received
        timeline_tweets = api.user_timeline(screen_name='user_id', tweet_mode="extended", count="200", max_id=oldest)

if __name__ == '__main__':
    # connecting to mySQL database and return connection and cursor for executing commands
    connection, cursor = connect_database()
    # authenticate via tweepy and return auth and api to stream tweets from users or locations
    auth, api = authenticate()

    stream_max_tweets = 2  # number of tweets streaming will pull in for user, or location method

    # filter stream by type location, send authenticated, string location, and bounding box location
    # [-137, 25, -59, 59] = bounding box around USA AND CANADA

    # stream_tweets_location(auth, [-137, 25, -59, 59])

    # filter stream by type user returns user tweets and others tweeting at user, mentions, and much more
    # 44196397 = elon musk

    # stream_tweets_user(auth, "44196397")

    # get user time line by sending in username and api from authenticate, optional 3rd argument for number of tweets
    # want returned, defaulted to maximum possible return of 3200 tweets

    # get_timeline_user("@elonmusk", api)

    # once complete will close connection to database and quit
    cursor.close()
    connection.close()
    quit()
