from __future__ import annotations
from marshmallow import Schema
from marshmallow.fields import Str, Int, List, Nested

from .user import UserSchema


class CommentSchema(Schema):
    content = Str(required=False)
    like = Int()
    author = Nested(UserSchema(only=("name",)))
    next_comment = List(Nested("CommentSchema", many=True))


class TagSchema(Schema):
    name = Str(required=True)


class PostSchema(Schema):
    title = Str(required=True)
    author = Nested(UserSchema(only=("name",)))
    content = Str(required=True)
    tags = List(Nested(TagSchema()))
    comments = Nested(CommentSchema())


class CategorySchema(Schema):
    name = Str(required=True)
    posts = List(
        Nested(
            PostSchema(
                only=(
                    "title",
                    "author",
                )
            )
        )
    )
