import os
from flask_pymongo import pymongo

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

client = pymongo.MongoClient(f"mongodb+srv://user026:{DB_PASSWORD}@cluster0.ypown.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")
db = client.api_tv_shows
