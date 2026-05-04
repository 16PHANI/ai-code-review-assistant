from pymongo import MongoClient
from bson import ObjectId
import os

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["code_review_db"]
collection = db["reviews"]


def save_review(doc: dict) -> str:
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def get_reviews(session_id: str) -> list:
    docs = collection.find(
        {"session_id": session_id}, {"code": 0}
    ).sort("submitted_at", -1).limit(20)
    result = []
    for doc in docs:
        doc["id"] = str(doc.pop("_id"))
        result.append(doc)
    return result


def get_review_by_id(review_id: str) -> dict:
    try:
        doc = collection.find_one({"_id": ObjectId(review_id)})
    except Exception:
        return None
    if not doc:
        return None
    doc["id"] = str(doc.pop("_id"))
    return doc
