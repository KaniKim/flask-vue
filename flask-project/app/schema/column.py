from marshmallow import fields, Schema

from app.schema.user import UserSchema

class ColumnSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    like = fields.Int()
    author = fields.Nested(UserSchema())
    tags = fields.List(fields.Str())

class BoardSchema(Schema):
    columns = fields.List(fields.Nested(ColumnSchema()))
    name = fields.Str()