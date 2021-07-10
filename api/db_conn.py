from dotenv import dotenv_values
import mysql.connector

class Database:
    """
    This class is used to connect to a database
    TODO: before using the class you need to have a .env file in the folder in which this class is imported from 
    TODO: make sure the .env file has the following <key:value> pairs 
    DB_USERNAME=<database user>
    DB_PASSWORD=<password>
    DB_HOST=<localhost or other>
    DB_NAME=<database name within the DBMS>
    ...

    Attributes
    ----------
    config : OrderedDicdb
        a ordered dictionary of extracted key value pairs in the .env file
    db_connection : CMySQLConnection object
        mysql connection object or string memory location
    username :str
        db user
    password: str
        db password
    host: str
        hostname
    db_name: str
        db name within the DBMS
    Methods
    -------
    get_connection()
    run_query()
    """
    def __init__(self):
        self.config = dotenv_values(".env")
        self.db_connection = None

        if bool(self.config):
            self.username = self.config["DB_USERNAME"]
            self.password = self.config["DB_PASSWORD"]
            self.host = self.config["DB_HOST"]
            self.db_name = self.config["DB_NAME"]
        else:
            raise Exception("Error: Either File not found or Parsing error\n1. Check filename \".env\" and keyvalue pairs")
                
    def get_connection(self):
        """
            on success: mysql connection (CMySQLConnection object)
            on failure: False
        """
        if self.db_connection is None or self.db_connection.is_connected() is False:
            self.db_connection = mysql.connector.connect(
                user=self.username,
                password=self.password,
                host=self.host,
                database=self.db_name
            )
            if not self.db_connection.is_connected():
                print("Failed to connect with given credentials")
                return False
            return self.db_connection
        else:
            return self.db_connection
    
    def run_query(self, query):
        """
            on success: python list of query results
            on failure: {"error": "error message"}
        """
        # execute query
        try:
            conn = self.get_connection()
            db_cursor = conn.cursor()
            db_cursor.execute(query)
            results = db_cursor.fetchall()
            conn.commit()
            db_cursor.close()
            return results
        except mysql.connector.Error as error:
            return {"error": error.msg}


            