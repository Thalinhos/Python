import pymongo

uri = "seudominiio@bol.com"

client = pymongo.MongoClient(uri)

db = client.user

collection = db.user
#Não fechar client.close(), pois preciso dele aberto no script seguinte.
