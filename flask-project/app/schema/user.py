from marshmallow import fields, Schema

class UserSignUpSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    password = fields.Str()

class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    email = fields.Email()
    password = fields.Str()
    activated = fields.Bool()