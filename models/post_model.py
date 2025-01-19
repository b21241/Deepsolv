from pymongo import MongoClient
import datetime

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client['instagram_clone']
posts_collection = db['posts']

def create_post(username, description, image_url=''):
    post = {
        "username": username,
        "description": description,
        "image_url": image_url,
        "date": datetime.datetime.utcnow(),
    }
    posts_collection.insert_one(post)
    return post

def get_all_posts():
    return list(posts_collection.find().sort('date', -1))
