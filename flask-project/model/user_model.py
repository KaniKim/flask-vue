from . import db


class User(db.Document):
    name = db.StringField(max_length=255, required=True)
    email = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    activated = db.BooleanField(default=True)
