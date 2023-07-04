from conn import pymongo, collection, client
import read
from bson.objectid import ObjectId

read.read_data()

id = input('Escolha o id somente em números para a exclusão: ')
filtro = {'_id': ObjectId(id)}
print('')

try:
    print('Voce tem certeza que gostaria de excluir esse registro?')
    option = int(input("'1' para Sim, '2' para Não: "))

    if option == 1:
        collection.delete_one(filtro)
    else:
        print('Nenhuma alteração fora feita')

except:
    print('Erro')
finally:
    client.close()