from pymongo import MongoClient
from app.config import MONGO_URI
from app.external_services.db import DB

client = MongoClient(MONGO_URI)
db_instance = DB(client=client)

def get_db() -> DB:
    return db_instance