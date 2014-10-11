from pymongo import MongoClient

class MongoConnection(object):

    def __init__(self, host='127.0.0.1', db='local', collection='sample'):
        self.host = 'mongodb://' + host
        self.client = MongoClient(self.host)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def connect(self, host):
        self.host = host
        self.client = MongoClient(self.host)
        return self

    def use_collection(self, collection_name):
        self.collection = self.db[collection_name]
        return self.collection

    def use_db(self, db_name):
        self.db = self.client[db_name]
        return self.db