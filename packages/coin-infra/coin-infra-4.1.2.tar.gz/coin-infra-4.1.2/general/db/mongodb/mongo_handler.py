from pymongo import MongoClient


class MongoHandler:
    def __init__(self, host, port, username=None, password=None, auth_db="admin"):
        self.client = self._connect(host, port, username, password, auth_db)
        self.db = None
        self.collection = None

    def _connect(self, host, port, username, password, auth_db):
        if username and password:
            connection_uri = f"mongodb://{username}:{password}@{host}:{port}/{auth_db}"
        else:
            connection_uri = f"mongodb://{host}:{port}/"
        return MongoClient(connection_uri)

    def set_database(self, db_name):
        self.db = self.client[db_name]

    def set_collection(self, collection_name):
        if self.db is None:
            raise Exception("Database is not set. Use set_database() method first.")
        self.collection = self.db[collection_name]

    def insert(self, data):
        if self.collection is None:
            raise Exception("Collection is not set. Use set_collection() method first.")
        return self.collection.insert_one(data).inserted_id

    def insert_many(self, data_list):
        if self.collection is None:
            raise Exception("Collection is not set. Use set_collection() method first.")
        return self.collection.insert_many(data_list).inserted_ids

    def find(self, query=None):
        if self.collection is None:
            raise Exception("Collection is not set. Use set_collection() method first.")
        return list(self.collection.find(query))
