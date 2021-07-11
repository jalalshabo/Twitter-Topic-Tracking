from db_conn import Database
from dateutil.parser import parse

class TweetFactory:
    """
    This class is used to retrieve tweets from the database based on given filters
    This is a DAL class
    ...

    Attributes
    ----------
    db: db class 
        This is the database

    Methods
    -------
    tweets_by_date_range(start_date, end_date)
    tweets_by_user(user_id, start_date, end_date)

    """
    def __init__(self):
        self.db = Database()
    
    def is_validate_date(self,date):
        """
        checks a given string for validate date 
        on success: True
        on failure: False
        """
        try:
            parse(date)
            return True
        except ValueError:
            return False

    def tweets_by_date_range(self, start_date, end_date):
        """
        on success: json of tweets in daterange from db
        on failure: json with error message
        """
        # validate input dates
        if (not self.is_validate_date(start_date)) or (not self.is_validate_date(end_date)):
            return {"error": "invalid date"}
        
        # validate date range
        if (parse(start_date) > parse(end_date)):
            return {"error": "invalid date range"}
        
        # retrieve tweets in date range
        query = f'SELECT tweetId, tweetText FROM tweets_table WHERE tweetDate BETWEEN \'{start_date} 00:00:00\' and \'{end_date} 23:59:59\''
        data = self.db.run_query(query)
        return data
    def tweets_by_user(self, user_id, start_date, end_date):
        """
        Retrieves a specific users tweets within a date range
        on success: json of a users tweets in date range from db
        on failure: json with error message 
        """
        # validate input dates
        # validate input dates
        if (not self.is_validate_date(start_date)) or (not self.is_validate_date(end_date)):
            return {"error": "invalid date"}
        
        # validate date range
        if (parse(start_date) > parse(end_date)):
            return {"error": "invalid date range"}

        #validate userId
        if (not user_id.isdigit()):
            return {"error": "invalid userId"}

        # retrieve tweets for user in the date range
        query = f'SELECT tweetId, tweetText FROM tweets_table WHERE tweetDate BETWEEN \'{start_date} 00:00:00\' and \'{end_date} 23:59:59\' and userId={user_id}'
        data = self.db.run_query(query)
        return data

    # def tweets_by_date(self, date):
    #     """
    #     on success: json of tweets in date from db
    #     on failure: json with error message
    #     """
    #     # validate input date
    #     if (not self.is_validate_date(date)):
    #         return {"error": "invalid date"}
        
    #     # retrieve tweeets for date
    #     query =  f'SELECT tweetId, tweetText FROM tweets_table WHERE tweetDate BETWEEN \'{date} 00:00:00\' and \'{date} 23:59:59\''
    #     data = self.db.run_query(query)
    #     return data
