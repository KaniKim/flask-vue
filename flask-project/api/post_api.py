from __future__ import annotations

from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace
from flask_restx.fields import String, Integer, Nested, List, Raw

from bson.objectid import ObjectId
import json

from .user_api import UserModel
from ..model.user_model import User as UserMongo
from ..model.post_model import Post as PostMongo
from ..model.post_model import Comment as CommentMongo
from ..model.post_model import Tag as TagMongo
from ..model.post_model import Category as CategoryMongo

Post = Namespace("Post", description="CRUD for Post API")
Comment = Namespace("Comment", description="CRUD for Comment API")
Tag = Namespace("Tag", description="CRUD for Tag API")
Category = Namespace("Category", description="CRUD for Category API")

CommentModel = Comment.model(
    "comment",
    {
        "content": String,
        "like": Integer,
        "author": Nested(UserModel),
        "next_comment": Raw(title="comment"),
    },
)

TagModel = Tag.model("tag", {"name": String})

PostModel = Post.model(
    "post",
    {
        "_id": String,
        "title": String,
        "author": Nested(UserModel),
        "content": String,
        "tags": List(Nested(TagModel)),
        "comments": List(Nested(CommentModel)),
    },
)

CategoryModel = Category.model(
    "category", {"name": String, "posts": List(Nested(PostModel))}
)


@Post.route("")
class PostAll(Resource):
    @Post.marshal_with(PostModel, code=200)
    def get(self):
        if PostMongo.objects is None:
            return None

        return [json.loads(user.to_json()) for user in PostMongo.objects()]

    @Post.marshal_with(PostModel, code=201)
    def post(self):
        data = request.authorization

        import ipdb

        ipdb.set_trace()

        if "username" not in data or "password" not in data:
            return make_response(jsonify("No User Data"), 404)

        if (
            UserMongo.objects.filter(name=data["username"])[0].password
            != data["password"]
        ):
            return make_response(jsonify("Wrong Password or Username"), 404)

        title = request.get_json()["title"]
        author = UserMongo.objects.filter(name=data["username"])[0]
        content = request.get_json()["content"]
        tags = [TagMongo(name=tag) for tag in request.get_json()["tags"]]
        comments = []

        for tag in tags:
            tag.save()

        PostMongo(
            title=title, author=author, content=content, tags=tags, comments=comments
        ).save()

        return {
            "title": title,
            "author": author,
            "content": content,
            "tags": tags,
            "comments": [],
        }


@Category.route("")
class CategoryAll(Resource):
    @Category.marshal_with(CategoryModel, code=200)
    def get(self):
        pass


@Tag.route("/<string:post_id>")
class TagAll(Resource):
    @Tag.marshal_with(TagModel, code=200)
    def get(self, post_id: str):

        posts = PostMongo.objects.get(id=ObjectId(post_id))

        return [
            tag.to_mongo()
            for tag in TagMongo.objects.filter(name__in=posts.to_mongo()["tags"])
        ]


@Comment.route("")
class CommentAll(Resource):
    @Comment.marshal_with(CommentModel, code=200)
    def get(self):
        pass
