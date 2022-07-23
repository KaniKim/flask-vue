from marshmallow import fields, Schema

from app.schema.user import UserSchema

class ColumnSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    like = fields.Int()
    author = fields.Nested(UserSchema())
    tags = fields.List(fields.Str())

class ColumnBoardSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    tags = fields.List(fields.Str())
    name = fields.Str()

class ColumnAllSchema(Schema):
    columns = fields.List(fields.Nested(ColumnSchema()))

class BoardSchema(Schema):
    columns = fields.List(fields.Nested(ColumnSchema()))
    name = fields.Str()