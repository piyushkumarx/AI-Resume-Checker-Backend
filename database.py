from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

db = client["resume_ai_db"]

users_collection = db["users"]
resumes_collection = db["resumes"]