from pymongo import MongoClient
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()

mongo_user = quote_plus(os.getenv("MONGO_USER"))
mongo_password = quote_plus(os.getenv("MONGO_PW"))
mongo_app = quote_plus(os.getenv("MONGO_APP"))
mongo_host = quote_plus(os.getenv("MONGO_HOST"))

CONNECTION_STRING = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_host}/?appName={mongo_app}"

DB_NAME = "DUNGEON_DIARY"

def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client[DB_NAME]

db = get_database()

user_collection = db["users"]
campaign_collection = db["campaigns"]
notes_collection = db["notes"]