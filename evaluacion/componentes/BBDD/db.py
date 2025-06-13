from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="netscanner_db", collection_name="detailed_hosts"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_all_docs(self):
        # Retorna la lista de documentos
        return list(self.collection.find({}))

    def get_doc_by_ip(self, ip: str):
        # Retorna un documento filtrado por IP
        return self.collection.find_one({"ip": ip})
