from marshmallow import fields, Schema

class ColumnSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    content = fields.Str()
    like = fields.Int()
    author = fields.Str()
    tags = fields.List(fields.Str())

class LikeSchema(Schema):
    like = fields.Str()

class ColumnBoardSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    tags = fields.List(fields.Str())
    name = fields.Str()

class NextCommentSchema(Schema):
    content = fields.Str()
    author = fields.Str()

class CommentSchema(Schema):
    content = fields.Str()
    author = fields.Str()
    next_comment = fields.List(fields.Nested(NextCommentSchema()))

class ListCommentSchema(Schema):
    comments = fields.List(fields.Nested(CommentSchema()))

class ColumnAllSchema(Schema):
    columns = fields.List(fields.Nested(ColumnSchema()))

class BoardSchema(Schema):
    columns = fields.List(fields.Nested(ColumnSchema()))
    name = fields.Str()