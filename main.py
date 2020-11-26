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
        "message": "API working ok"
    })


if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)