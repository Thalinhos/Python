from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token":access_token})

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as":current_user}), 200


if __name__ == "__main__":
    app.run()

# POST http://127.0.0.1:5000/login HTTP/1.1
# content-type: application/json

# {
#     "username": "test",
#     "password": "test"
# }
# ###

# GET http://127.0.0.1:5000/protected HTTP/1.1
# Authorization: Bearer eyJshbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTUxMDU0MCwianRpIjoiY2YxYjg2YTMtNzA1Yy00ZjZjLWJjZWEtZjViNmRkZDNlZTdiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QiLCJuYmYiOjE3MzE1MTA1NDAsImNzcmYiOiI0NzI0ODQzZC04NzAxLTQwODItYTA5OS1hOTlmNjFlYTMzNDIiLCJleHAiOjE3MzE1MTE0NDB9.LEgnyqHr7DkvICn9RbcLI1N1lJzGVRmdMZBULnIL_9A
