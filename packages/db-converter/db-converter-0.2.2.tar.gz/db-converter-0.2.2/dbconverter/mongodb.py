import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoDb:

    def __init__(self, uri):
        """
        Initializes the MongoDb class with the provided URI.

        Args:
            uri (str): The URI for connecting to the MongoDB instance.
        """
        self.client = None
        self.db = None
        self.collection = None
        self.uri = uri

    def connect(self):
        """
        Establishes a connection to the MongoDB instance.
        """
        # Connect to MongoDB
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client['crypto']

    @staticmethod
    def df_to_json(df) -> list:
        """
        Converts a DataFrame to a list of JSON documents.

        Args:
            df (pd.DataFrame): The DataFrame to be converted.

        Returns:
            list: A list of JSON documents.
        """
        # Convert each row to a JSON document
        json_docs = []
        for index, row in df.iterrows():
            json_doc = row.to_dict()  # Convert row to dictionary
            json_docs.append(json_doc)
        return json_docs

    def insert_json(self, json_data, collection):
        """
        Inserts a JSON document into the specified collection.

        Args:
            json_data (dict): The JSON document to be inserted.
            collection (str): The name of the collection to insert into.
        """
        try:
            self.connect()
            self.collection = self.db[collection]
            # Insert data
            insert_result = self.collection.insert_one(json_data)
            print('Eklenen belge ID:', insert_result.inserted_id)
            self.client.close()
        except Exception as e:
            print("Insert_data Error: ", e)

    def insert_data(self, df, collection):
        """
        Inserts data from a DataFrame into the specified collection.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be inserted.
            collection (str): The name of the collection to insert into.
        """
        json_docs = self.df_to_json(df)

        # Insert documents
        for json_doc in json_docs:
            self.insert_json(json_doc, collection)
            print(json_doc)

    def get_data(self, collection, query=None):
        """
        Retrieves data from the specified collection.

        Args:
            collection (str): The name of the collection to retrieve data from.
            query (dict): The query to filter the data (optional).

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved data.
        """
        self.connect()
        if query is None:
            # Retrieve data
            my_collection = self.db[collection]
            data = list(my_collection.find())
            df = pd.DataFrame(data)
            self.client.close()
            return df
        else:
            my_collection = self.db[collection]
            data = my_collection.find(query)
            df = pd.DataFrame(data)
            self.client.close()
            return df

    def check_collection_name(self, collection_name):
        """
        Checks if a collection with the specified name exists.

        Args:
            collection_name (str): The name of the collection to check.

        Returns:
            bool: True if the collection exists, False otherwise.
        """
        self.connect()

        # Check if collection exists
        if collection_name in self.db.list_collection_names():
            print(f"'{collection_name}' koleksiyonu mevcut.")
            return True
        else:
            print(f"'{collection_name}' koleksiyonu mevcut değil.")
            return False

        self.client.close()

    def create_collection(self, collection_name):
        """
        Creates a new collection with the specified name.

        Args:
            collection_name (str): The name of the new collection to create.
        """
        self.connect()

        # Create collection
        collection = self.db[collection_name]
        self.client.close()
