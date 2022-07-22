import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField

class UserModel(Document):
    name = StringField(max_length=255, required=True)
    email = StringField(max_length=255, required=True)
    password = StringField(max_length=255, required=True)
    activated = BooleanField(default=True)
    created_at = DateTimeField(defualt=datetime.datetime.utcnow())
    deleted_at = DateTimeField()
