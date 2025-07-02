import pymongo

class MongoDBHandler:
    def __init__(self, host="localhost", port=27020, db_name="testdb", collection_name="records"):
        self.client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def clear_collection(self):
        self.collection.delete_many({})

    def insert_documents(self, docs):
        self.collection.insert_many(docs)
