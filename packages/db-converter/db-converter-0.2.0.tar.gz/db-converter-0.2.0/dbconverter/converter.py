from mongodb import MongoDb
from MySQLConnector import MySQLConnector


class converter:
    def __init__(self, mongo_uri, **kwargs):
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
        :param mysql_bilgilerim:
        :param mongodb_bilgilerim:
        :param table_name:
        :return:
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
        :param mysql_bilgilerim:
        :param mongodb_bilgilerim:
        :param collection_name:
        :return:
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
