from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_apispec import MethodResource

import jwt

from ..config import Config
from ..repository.post import PostRepository
from ..repository.user import UserRepository
from ..repository.category import CategoryRepository

post_repo = PostRepository()
user_repo = UserRepository()
category_repo = CategoryRepository()


class Auth:
    @classmethod
    def get_header(cls, header):
        if header is None:
            return 404

        try:
            current_user = jwt.decode(header, Config.key, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            return 400

        if "username" not in current_user:
            return 404
        return current_user


class Category(MethodResource, Resource):
    def get(self):

        current_user = Auth().get_header(header=request.headers.get("Authorization"))

        if isinstance(current_user, int):
            return make_response(jsonify("Token Expired"), current_user)

        if user_repo.find_user_by_email(current_user["username"]) is None:
            return make_response(jsonify({"msg": "Plz Login"}, 404))

        return category_repo.find_all_category()


class PostComment(MethodResource, Resource):
    def get(self):

        Auth().get_header(header=request.headers.get("Authorization"))


class Post(MethodResource, Resource):
    def post(self):

        current_user = Auth().get_header(header=request.headers.get("Authorization"))

        if isinstance(current_user, int):
            return make_response(jsonify("Token Expired"), current_user)

        title = request.get_json()["title"]
        author = current_user["username"]
        content = request.get_json()["content"]
        tags = request.get_json()["tags"]
        category = request.get_json()["category"]
        comments = []

        post_repo.save_post(title, author, content, tags, comments, category)

        return make_response(jsonify({"msg": "Post is Written"}), 201)

    def get(self):
        current_user = Auth().get_header(header=request.headers.get("Authorization"))

        if isinstance(current_user, int):
            return make_response(jsonify("Token Expired"), current_user)

        return post_repo.find_posts_by_category(request.args.get("category_name"))
