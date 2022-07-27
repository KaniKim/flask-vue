from marshmallow import fields, Schema

class UserLoginSchema(Schema):
    jwt = fields.Str()

class UserSignUpSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(reuqired=True)
    password = fields.Str(required=True)

class UserSchema(Schema):
    _id = fields.Str()
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    activated = fields.Bool()
