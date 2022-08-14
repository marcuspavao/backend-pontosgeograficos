from flask import Flask, Response, request
import pymongo    
import json
from bson import ObjectId

app = Flask(__name__)

def mongo_connection():
    try:
        mongo = pymongo.MongoClient(
            host="localhost",
            port= 27017,
            serverSelectionTimeoutMS = 1000
        )
        db = mongo.company
        return db
    except:
        print("ERROR - Não pode connectar")

db = mongo_connection()

class Pontos:
    def __init__(self, latitude, longitude, descricao):
        self.latitude = latitude
        self.longitude = longitude
        self.descricao = descricao

class Usuario:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



@app.route("/VerPontos", methods=["GET"])
def getPontos():
    try:
        data = list(db.pontos.find())
        ##for p in data:
          #  p["_id"] = str(p["_id"])
        return Response(
            response= JSONEncoder().encode(data),
            status = 200,
            mimetype= "application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({
                "message": "Can't read user"
                }),
            status = 500,
            mimetype= "application/json"
        )


@app.route("/AdicionarPonto/", methods=["POST"])
def addPonto():
    try:
        longitude = request.args.get('longitude')
        descricao = request.args.get('descricao')
        latitude = request.args.get('latitude')
        email = request.args.get('email')
        data = db.users.find_one({"email": email})
        if data:
            ponto  = Pontos(latitude,longitude,descricao)
            db.Response = db.pontos.insert_one(ponto.__dict__)
            return Response(
                response= json.dumps({
                    "message": "Ponto created", 
                    "id": f"{db.Response.inserted_id}"}),
                status = 201,
                mimetype= "application/json"
            )
    except Exception as ex:
        print(ex)

@app.route("/RemoverPonto/", methods=["DELETE"])
def deletePonto():
    try:
        id = request.args.get('id')
        user = request.args.get('user')
        db.Response = db.pontos.find_one_and_delete({"_id": ObjectId(id) })
        if(db.Response):
            return Response(
                response= json.dumps({
                    "message": "Ponto deleted"}),
                status = 200,
                mimetype= "application/json"
            )
    except Exception as ex:
        print(ex)

@app.route("/AdicionarUsuario/", methods=["POST"])
def addUser():
    try:
        print(db.list_collection_names())
        nome = request.args.get('nome')
        email = request.args.get('email')
        user  = Usuario(nome,email)
        print(user.__dict__)
        db.Response = db.users.insert_one(user.__dict__)
       
        return Response(
            response= json.dumps({
                "message": "User created", 
                "id": f"{db.Response.inserted_id}"}),
            status = 201,
            mimetype= "application/json"
        )
    except Exception as ex:
        print(ex)


@app.route("/RemoverUsuario/", methods=["DELETE"])
def deleteUser():
    try:
        email = request.args.get('email')
        db.Response = db.users.find_one_and_delete({"email": email})
        if(db.Response):
            return Response(
                response= json.dumps({
                    "message": "User deleted"}),
                status = 200,
                mimetype= "application/json"
            )
    except Exception as ex:
        print(ex)

@app.route("/VerUsuarios", methods=["GET"])
def getUsers():
    try:
        data = list(db.users.find())
        print(data)
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response= json.dumps(data),
            status = 200,
            mimetype= "application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({
                "message": "Can't read user"
                }),
            status = 500,
            mimetype= "application/json"
        )


@app.route("/")
def route1():
    return "Backend Python Dados Geográficos"

if __name__ == "__main__":
    app.run(port=8080, debug=True)


#def home():
#    return render_template("home.html")