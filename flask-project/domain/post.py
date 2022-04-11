from __future__ import annotations
from marshmallow import Schema, fields

from .user import UserSchema


class CommentSchema(Schema):
    content = fields.String(required=False)
    like = fields.Integer()
    author = fields.Nested(UserSchema(only=("name",)))
    next_comment = fields.List(
        fields.Nested(lambda: CommentSchema(exclude="next_comment"), many=True)
    )


class TagSchema(Schema):
    name = fields.String(required=True)


class PostSchema(Schema):
    title = fields.String(required=True)
    author = fields.Nested(UserSchema(only=("name",)))
    content = fields.String(required=True)
    tags = fields.List(fields.Nested(TagSchema()))
    comments = fields.Nested(CommentSchema())


class CategorySchema(Schema):
    name = fields.String(required=True)
    posts = fields.List(
        fields.Nested(
            PostSchema(
                only=(
                    "title",
                    "author",
                )
            )
        )
    )
