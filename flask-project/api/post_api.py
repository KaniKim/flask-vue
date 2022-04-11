from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_apispec import MethodResource, marshal_with
from flask_jwt_extended import jwt_required

import json

from ..domain.post import PostSchema
from ..model.user_model import User as UserMongo
from ..model.post_model import Post as PostMongo
from ..model.post_model import Tag as TagMongo
from ..model.post_model import Category as CategoryMongo


class Post(MethodResource, Resource):
    @jwt_required
    def post(self):
        data = request.get_json()

        if "username" not in data and "password" not in data:
            return make_response(jsonify("No User Data"), 404)

        if (
            UserMongo.objects.filter(email=data["username"])[0].password
            != data["password"]
        ):
            return make_response(jsonify("Wrong Password or Username"), 404)
        import ipdb

        ipdb.set_trace()

        title = request.get_json()["title"]
        author = UserMongo.objects.filter(email=data["username"])[0]
        content = request.get_json()["content"]
        tags = [TagMongo(name=tag) for tag in request.get_json()["tags"]]
        category = request.get_json()["category"]
        comments = []

        for tag in tags:
            tag.save()

        post = PostMongo(
            title=title, author=author, content=content, tags=tags, comments=comments
        ).save()
        CategoryMongo(name=category, posts=[post]).save()
        return make_response(jsonify({"msg": "Post is Written"}), 201)

    @marshal_with(PostSchema, code=200)
    def get(self):
        if PostMongo.objects is None:
            return None

        return [json.loads(user.to_json()) for user in PostMongo.objects()]


class Category(Resource):
    def get(self, category_name: str):
        posts = CategoryMongo.objects.filter(name=category_name)[0].posts

        posts_model = [PostMongo.objects.filter(id=post.id)[0] for post in posts]
        return [
            {
                "title": post.title,
                "author": json.loads(
                    UserMongo.objects.filter(id=post.author.id)[0].to_json()
                ),
                "tags": [
                    json.loads(TagMongo.objects.filter(id=tag.id)[0].to_json())
                    for tag in post.tags
                ],
            }
            for post in posts_model
        ]
