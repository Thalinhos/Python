from conn import pymongo, collection, client
import read
from bson.objectid import ObjectId

read.read_data()

id = input('Escolha o id somente em números: ')
filtro = {'_id': ObjectId(id)}
print('')

print("'1' para editar o campo name")
print("'2' para editar o campo last_name")
option = int(input('Digite sua opção em numeros: '))
print('')

try:
    if option == 1:
        new_name = input('Digite o novo name: ')
        att_name = { '$set': { "name": new_name }}
        collection.update_one(filtro, att_name)
    elif option == 2:
        new_last_name = input('Digite o novo lastname: ')
        att_last_name = { '$set': { "last_name": new_last_name }}
        collection.update_one(filtro, att_last_name)
    else:
        print('Erro, nenhuma ação fora concluida.')
except:
    print('Erro')

finally:
    client.close()



















    