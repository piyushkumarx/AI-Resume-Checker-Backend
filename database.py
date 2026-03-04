from pymongo import MongoClient

MONGO_URL = "mongodb+srv://khushihackerx:Khushi%231234@cluster0.cmhfs8j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URL)

db = client["resume_ai_db"]

users_collection = db["users"]
resumes_collection = db["resumes"]


