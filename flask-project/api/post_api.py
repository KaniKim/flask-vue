from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_apispec import MethodResource

import jwt

from ..config import Config
from ..repository.post import PostRepository
from ..repository.user import UserRepository

post_repo = PostRepository()
user_repo = UserRepository()


class Post(MethodResource, Resource):
    def post(self):

        header = request.headers.get("Authorization")

        if header is None:
            return make_response(jsonify({"msg": "Plz Login"}, 404))

        current_user = jwt.decode(header, Config.key, algorithms="HS256")

        if "username" not in current_user:
            return make_response(jsonify("No User Data"), 404)

        title = request.get_json()["title"]
        author = current_user["username"]
        content = request.get_json()["content"]
        tags = request.get_json()["tags"]
        category = request.get_json()["category"]
        comments = []

        post_repo.save_post(title, author, content, tags, comments, category)

        return make_response(jsonify({"msg": "Post is Written"}), 201)

    def get(self, category_name: str):
        return post_repo.find_posts_by_category(category_name)
