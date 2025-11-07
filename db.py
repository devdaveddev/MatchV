
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["matchmaking"]

names_collection = db["names"]
