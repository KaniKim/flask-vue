from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from .model import db
from .api.user_api import User
from .api.post_api import Post, Comment, Category, Tag

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    "db": "test",
    "username": "kani",
    "password": "123456",
    "host": "mongodb",
    "port": 27017,
}

CORS(app)

api = Api(app)
api.add_namespace(User, "/user")
api.add_namespace(Post, "/post")
api.add_namespace(Comment, "/comment")
api.add_namespace(Category, "/category")
api.add_namespace(Tag, "/tag")

db.init_app(app)
