from mongoengine import Document, StringField, IntField, ReferenceField, ListField, LazyReferenceField
from app.model.user import UserModel


class TagModel(Document):
    name = StringField(max_length=255, required=True)


class CommentModel(Document):
    content = StringField(max_length=255, required=True)
    like = IntField(default=0)
    author = ReferenceField(UserModel)
    next_comment = ListField(LazyReferenceField("self"))


class ColumnModel(Document):
    title = StringField(max_length=255, required=True)
    author = ReferenceField(UserModel)
    content = StringField()
    like = IntField(default=0)
    tags = ListField(ReferenceField(TagModel))
    comments = ListField(LazyReferenceField(CommentModel))


class BoardModel(Document):
    columns = ListField(LazyReferenceField(ColumnModel))
    name = StringField(max_length=255, required=True)
