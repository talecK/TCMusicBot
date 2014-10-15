from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoConnection(object):

    """ Manages Mongodb connections

    Args:
        host (string, optional): the ip or named address to locate the mongodb instance. Defaults to localhost(127.0.0.1).
        db (string): the name of the database to connect to. Default is local.
        collection (string): the name of the collection to use. Default is sample.
    """
    def __init__(self, host='127.0.0.1', db='local', collection='sample'):
        self.host = 'mongodb://' + host
        self.client = MongoClient(self.host)
        self.db = self.client[db]
        self.collection = self.db[collection]

    def connect(self, host):
        """ Makes connection to mongodb instance

        Args:
            host (string): ip or named address to the mongodb instance

        Returns:
            self (MongoConnection)
        """
        self.host = host
        self.client = MongoClient(self.host)
        return self

    def use_collection(self, collection_name):
        """ Switches mongo connection to begin using a specific collection.

        Args:
            collection_name (string): name of the collection to be used.

        Returns:
            self.collection (dict): the dictionary containing the mongodb collection of documents.
        """
        self.collection = self.db[collection_name]
        return self.collection

    def use_db(self, db_name):
        """ Switches mongo connection to begin using a specific database.

        Args:
            db_name (string): name of the database to be used.

        Returns:
            self.db (dict): the dictionary containing the database of collections.
        """
        self.db = self.client[db_name]
        return self.db

    def get_key(self, id):
        """ Formats an id string into an ObjectId instance

        Args:
            id (string): database id to convert

        Returns:
            (ObjectId): the id converted into a mongo ObjectId.
        """
        return ObjectId(str(id))
