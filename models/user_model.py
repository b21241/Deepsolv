from pymongo import MongoClient
import hashlib

client = MongoClient("mongodb://localhost:27017/")
db = client['instagram_clone']
users_collection = db['users']

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(hashed_password, input_password):
    return hashed_password == hash_password(input_password)

def register_user(username, email, password):
    if users_collection.find_one({"username": username}):
        return {"error": "User already exists"}

    hashed_password = hash_password(password)
    user = {"username": username, "email": email, "password": hashed_password}
    users_collection.insert_one(user)
    return user

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if not user or not check_password(user['password'], password):
        return None
    return user
