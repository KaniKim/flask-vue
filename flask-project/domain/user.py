from marshmallow import Schema, fields, INCLUDE


class UserSchema(Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    activated = fields.Boolean(required=False, default=True)

    class Meta:
        unknown = INCLUDE
