from conn import pymongo, collection, client


name = input("Insira seu nome: ")
last_name = input("Insira seu sobrenome: ")

dados = {
    'name': name,
    'last_name': last_name
}   

try:
    collection.insert_one(dados)
    print('success')
except:
    print('error')
finally:
    client.close()

