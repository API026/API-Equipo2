from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__) # Crear API Flask
    CORS(app) # Aplicar cors a la API

    return app # Devolver la app creada