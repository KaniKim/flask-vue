from mongoengine import Document, StringField, BooleanField

class UserModel(Document):
    name = StringField(max_length=255, required=True)
    email = StringField(max_length=255, required=True)
    password = StringField(max_length=255, required=True)
    activated = BooleanField(default=True)
