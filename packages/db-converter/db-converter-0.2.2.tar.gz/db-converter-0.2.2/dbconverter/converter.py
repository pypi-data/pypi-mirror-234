from .mongodb import MongoDb
from .MySQLConnector import MySQLConnector


class dataconverter:
    def __init__(self, mongo_uri, **kwargs):
        """
        Initializes the Converter class.

        Args:
            mongo_uri (str): The URI for connecting to MongoDB.
            **kwargs: Keyword arguments containing MySQL connection details.
                      Expected keys: 'host', 'user', 'password', 'port', 'database'.
        """
        self.mongo_uri = mongo_uri

        self.host = kwargs['host']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.port = kwargs['port']
        self.database = kwargs['database']

        self.mysql_conn = MySQLConnector(self.host, self.user, self.password, self.port, self.database)
        self.mongo_conn = MongoDb(self.mongo_uri)

    def mysql_to_mongodb(self, table_name=None):
        """
        Migrates data from MySQL to MongoDB.

        Args:
            table_name (str, optional): The name of the table to migrate (default is None).
                                        If None, all tables will be migrated.

        Returns:
            None
        """

        if table_name is None:
            print("bütün db geçirelecek")
        else:
            df = self.mysql_conn.get_data(table_name)
            if self.mongo_conn.check_collection_name(table_name):
                self.mongo_conn.insert_data(df, table_name)
            else:  # Collection mevcut değil.
                self.mongo_conn.create_collection(table_name)
                self.mongo_conn.insert_data(df, table_name)

    def mongodb_to_mysql(self, collection_name=None):
        """
        Migrates data from MongoDB to MySQL.

        Args:
            collection_name (str, optional): The name of the collection to migrate (default is None).
                                             If None, all collections will be migrated.

        Returns:
            None
        """
        if collection_name is None:
            print("bütün db geçirelecek")
        else:
            df = self.mongo_conn.get_data(collection_name)
            if self.mysql_conn.check_table_name(collection_name):  # tablo varsa
                self.mysql_conn.insert_data(df, collection_name)
            else:  # tablo yoksa
                self.mysql_conn.create_table(table_name=collection_name, df=df)
                self.mysql_conn.insert_data(df, collection_name)
