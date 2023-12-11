from pymongo import MongoClient
class DatabaseUtility:

    def __init__(self, uri, dbName):
        self.uri = uri
        self.dbName = dbName

    def dataBaseConnection(self):

        client = MongoClient(self.uri)
        return client[self.dbName]