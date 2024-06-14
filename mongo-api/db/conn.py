from pymongo import MongoClient

class Connection:
    client = MongoClient('mongodb://admin:password@localhost:27017/')
    db = client['dbDiscordApi']

    def getDb():
        return Connection.db