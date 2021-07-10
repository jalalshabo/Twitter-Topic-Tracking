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
    tweets_by_date(date)
    tweets_by_user(user_id)

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

        print(f"start_date: {start_date}")
        print(f"end_date: {end_date}")

        # TODO: error handling 
        # TODO: add a fetchquery data function to DATABASE
        query = f'SELECT tweetId, tweetText FROM tweets_table WHERE tweetDate BETWEE {start_date} and \'{end_date} 23:59:59\''
        data = self.db.run_query(query)
        return data
        
