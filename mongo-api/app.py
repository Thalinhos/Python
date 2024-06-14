# from flask import Flask, jsonify, request
# app = Flask(__name__)

from services.userService import UserService
from services.serverService import ServerService
from services.userServerService import UserServerService


doc = {
    'name': 'arnaldo',
    'idade': 15
}

UserService.userService.insert_one(doc)

users = UserService.userService.find()

for u in users:
    print(u)



# print("Coleções no banco de dados:")
# for collection in collections:
#     print(collection)





     










