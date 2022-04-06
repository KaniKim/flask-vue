from . import db
from .user_model import User


class Tag(db.Document):
    name = db.StringField(max_length=255, required=True)


class Comment(db.Document):
    content = db.StringField(max_length=255, required=True)
    like = db.IntField()
    author = db.ReferenceField(User)
    next_comment = db.ReferenceField("self")


class Post(db.Document):
    title = db.StringField(max_length=255, required=True)
    author = db.ReferenceField(User)
    content = db.StringField()
    tags = db.ListField(db.ReferenceField(Tag))
    comments = db.ListField(db.ReferenceField(Comment))


class Category(db.Document):
    posts = db.ListField(db.ReferenceField(Post))
    name = db.StringField(max_length=255, required=True)
