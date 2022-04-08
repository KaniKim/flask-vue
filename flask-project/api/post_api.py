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


@Category.route("/<string:category_name>")
class CategorySpecific(Resource):
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


@Category.route("")
class CategoryAll(Resource):
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
