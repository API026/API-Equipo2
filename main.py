from os import name
from flask import jsonify, request
from flask_pymongo import pymongo
from app import create_app
from bson.json_util import dumps
import db_config as db

app = create_app() # Creación de la app

secretToken = "fnj934no58f" # Token secreto para los endpoints

@app.route('/test/') # EndPoint para testear la API
def test():
    return jsonify({
        "message": "API working ok " # Enviar mensaje de Ok
    })

@app.route('/api_tv_shows/shows/', methods=['GET']) # Obtener todos los shows de la base de datos
def show_mobs():
    
    shows = list(db.db.api_tv_shows.find())
    for show in shows: # Eliminar el dato _id (de Mongo)
        del show ["_id"]

    return jsonify({"All_shows":shows}) # Devolver un Json con la información

@app.route('/api_tv_shows/new_show/<string:tokenUser>', methods=['POST']) # Metodo post que necesita un JSON, y el secretToken
def add_new_show(tokenUser): # Creación de la función
    if tokenUser == secretToken: # Proceder si se ingresa correctamente el token
        db.db.api_tv_shows.insert_one({ # Insersión de los datos
            "name": request.json["name"],
            "category":request.json["category"],
            "imdb":request.json["imdb"],
            "top":request.json["top"],

        })
        return jsonify({ # Informar que se ingresaron correctamente
            "message":" Success",
            "status": 200,
        })
    else:
        return jsonify({ # Informar de que se ingreso un token erroneo
        "message":"Incorrect token  ",
        "status": 700,
    })

@app.route('/api_tv_shows/update_show/<string:tokenUser>/<string:name>', methods=['PUT']) # Método PUT que necesita el nombre del show y el token
def update_show(tokenUser,name): # Creación de la función
    if tokenUser == secretToken: # Proceder si se ingresa correctamente el token
        if db.db.api_tv_shows.find_one({'name':name}): # Buscar uno en la base de datos igual al nombre
            db.db.api_tv_shows.update_one({'name':name}, # Actualizar este con el JSON ingresado
            {'$set':{
                "name": request.json["name"],
                "category":request.json["category"],
                "imdb":request.json["imdb"],
                "top":request.json["top"]
            }})
        else:
            return jsonify({"status":400, "message": f"Show {name} not found"}) # No fue encontrado
        return jsonify({"status":200, "message": f"Show {name} was updated"}) # Fue actualizado
    else:
        return jsonify({ # Informar de que se ingreso un token erroneo
        "message":"Incorrect token ",
        "status": 700,
    })

@app.route('/api_tv_shows/show/del/<string:name>/<string:tokenUser>',methods=['DELETE']) # Función delete que recibe el nombre del show y el token
def delete_show(name, tokenUser): # Creación de la función
    if tokenUser == secretToken: # Proceder si se ingresa correctamente el token
        if db.db.api_tv_shows.find_one({'name':name}): # Encontrar el show a eliminar
            db.db.api_tv_shows.delete_one({'name':name}) # Eliminarlo
        else:
            return jsonify({"status":400, "message": f"Show {name} not found"}) # Informar que no fue encontrado
        return jsonify({"status":200, "message": f"Show {name} was deleted"}) # Informar que se elimino
    else:
        return jsonify({ # Informar de que se ingreso un token erroneo
        "message":"Incorrect token",
        "status": 700,
    })

if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080) # En que puerto se inicia (para local)