from conn import pymongo, collection, client
from bson.objectid import ObjectId

def read_data():
    try:
        documents = collection.find()
        for document in documents:
            print(document)
    except:
        print('error')
#Não fechar client.close(), pois preciso dele aberto no script seguinte.
