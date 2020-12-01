from os import name
from flask import jsonify, request
from flask_pymongo import pymongo
from app import create_app
from bson.json_util import dumps
import db_config as db

app = create_app()

secretToken = "fnj934no58f"

@app.route('/test/')
def test():
    return jsonify({
        "message": "API working ok "
    })

@app.route('/api_tv_shows/shows/', methods=['GET'])
def show_mobs():
    
    shows = list(db.db.api_tv_shows.find())
    for show in shows:
        del show ["_id"]

    return jsonify({"All_shows":shows})

@app.route('/api_tv_shows/new_show/<string:tokenUser>', methods=['POST'])
def add_new_show(tokenUser):
    if tokenUser == secretToken:
        db.db.api_tv_shows.insert_one({
            "name": request.json["name"],
            "category":request.json["category"],
            "imdb":request.json["imdb"],
            "top":request.json["top"],

        })
        return jsonify({
            "message":" Success",
            "status": 200,
        })
    else:
        return jsonify({
        "message":"Incorrect token  ",
        "status": 700,
    })

@app.route('/api_tv_shows/update_show/<string:tokenUser>/<string:name>', methods=['PUT'])
def update_show(tokenUser,name):
    if tokenUser == secretToken:
        if db.db.api_tv_shows.find_one({'name':name}):
            db.db.api_tv_shows.update_one({'name':name},
            {'$set':{
                "name": request.json["name"],
                "category":request.json["category"],
                "imdb":request.json["imdb"],
                "top":request.json["top"]
            }})
        else:
            return jsonify({"status":400, "message": f"show {name} not found"})
        return jsonify({"status":200, "message": f"show {name} was updated"})
    else:
        return jsonify({
        "message":"Incorrect token ",
        "status": 700,
    })

@app.route('/api_tv_shows/show/del/<string:name>/<string:tokenUser>',methods=['DELETE'])
def delete_show(name, tokenUser):
    if tokenUser == secretToken:
        if db.db.api_tv_shows.find_one({'name':name}):
            db.db.api_tv_shows.delete_one({'name':name})
        else:
            return jsonify({"status":400, "message": f"Show {name} not found"})
        return jsonify({"status":200, "message": f"Show {name} was deleted"})
    else:
        return jsonify({
        "message":"Incorrect token",
        "status": 700,
    })

if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)