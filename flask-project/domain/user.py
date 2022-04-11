from marshmallow import Schema, INCLUDE
from marshmallow.fields import Str, Bool


class UserSchema(Schema):
    name = Str(required=True)
    email = Str(required=True)
    password = Str(required=True)
    activated = Bool(default=True)

    class Meta:
        unknown = INCLUDE
