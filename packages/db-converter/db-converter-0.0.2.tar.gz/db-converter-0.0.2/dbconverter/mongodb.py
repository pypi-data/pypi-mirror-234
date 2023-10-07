import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoDb:

    def __init__(self, uri):

        self.client = None
        self.db = None
        self.collection = None
        self.uri = uri

    def connect(self):
        # MongoDB'ye bağlanma
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.db = self.client['crypto']

    @staticmethod
    def df_to_json(df) -> list:
        # DataFrame'i döngü ile dönerek her satırı ayrı bir JSON nesnesine dönüştür
        json_docs = []
        for index, row in df.iterrows():
            json_doc = row.to_dict()  # Satırı bir sözlüğe dönüştür
            json_docs.append(json_doc)
        return json_docs

    def insert_json(self, json_data, collection):
        try:
            self.connect()
            self.collection = self.db[collection]
            # Veri ekleme
            insert_result = self.collection.insert_one(json_data)
            print('Eklenen belge ID:', insert_result.inserted_id)
            self.client.close()
        except Exception as e:
            print("Insert_data Error: ", e)

    def insert_data(self, df, collection):
        json_docs = self.df_to_json(df)

        # BELGELERİ EKLİYOR ÇALIŞIYOR
        for json_doc in json_docs:
            self.insert_json(json_doc, collection)
            print(json_doc)

    def get_data(self, collection, query=None):
        self.connect()
        if query is None:
            # Veri çekme
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
        self.connect()

        # Koleksiyon var mı kontrol et
        if collection_name in self.db.list_collection_names():
            print(f"'{collection_name}' koleksiyonu mevcut.")
            return True
        else:
            print(f"'{collection_name}' koleksiyonu mevcut değil.")
            return False

        self.client.close()

    def create_collection(self, collection_name):
        self.connect()
        # Koleksiyon oluştur
        collection = self.db[collection_name]
        self.client.close()