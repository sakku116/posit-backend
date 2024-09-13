from pymongo import MongoClient
from pymongo.database import Database

from .env import Env


def getMongoDB() -> Database:
    conn = MongoClient(Env.MONGODB_URI)
    return conn[Env.MONGODB_NAME]

def newMongoDB(uri: str = Env.MONGODB_URI, name: str = Env.MONGODB_NAME) -> Database:
    conn = MongoClient(uri)
    return conn[name]
