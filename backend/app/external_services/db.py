import httpx
import json
from pymongo import MongoClient
from datetime import datetime, UTC

from app.models.db.user import User
from app.models.db.message import Message
from app.config import FIREBASE_DB_API, MONGO_URI

class DB:
    def __init__(self):
        self.mongo_uri = MONGO_URI
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client.get_default_database()
            self.users_collection = self.db["users"]
            self.messages_collection = self.db["messages"]
            print("Successfully connected to MongoDB.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None
            self.users_collection = None
            self.messages_collection = None
        self.headers = {
            'Content-Type': 'application/json',
        }
    
    async def track_message(self, response):
        json_str = json.dumps(response, default=str)
        timestamp = datetime.now(UTC).strftime("%d-%b-%Y-%H-%M-%S")
        url = f"{FIREBASE_DB_API}/solstrom/{timestamp}.json"
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=self.headers, json=json_str)
        return {"status": response.status_code, "data": response.json()}

    def get_user(self, user_id: str):
        if self.users_collection is None:
            return None
        return self.users_collection.find_one({"user_id": user_id})

    def get_user_by_email(self, email: str):
        if self.users_collection is None:
            return None
        return self.users_collection.find_one({"email": email})

    def create_user(self, user_id: str, email: str, name: str):
        if self.users_collection is None:
            return None
        user_data = User(user_id=user_id, email=email, name=name)
        self.users_collection.insert_one(user_data.model_dump())
        return user_data.model_dump()

    def update_user_paid(self, user_id: str):
        if self.users_collection is None:
            return
        self.users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"paid": True, "free": False}}
        )

    def set_user_paid(self, user_id: str):
        self.update_user_paid(user_id)

    def store_message(self, user_id: str, user_message: str, agent_message: str):
        if self.messages_collection is None:
            return None
        message_data = Message(
            user_id=user_id,
            user_message=user_message,
            agent_message=agent_message
        )
        self.messages_collection.insert_one(message_data.model_dump())
        return message_data.model_dump()

    def count_user_messages(self, user_id: str):
        if self.messages_collection is None:
            return 0
        return self.messages_collection.count_documents({"user_id": user_id})