from db.conn import Connection

class Model:
    db = Connection.getDb()

    collectionUsers = db['users']
    collectionServer = db['servers']
    collectionUsersServers = db['users_servers']