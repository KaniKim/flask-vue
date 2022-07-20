from mongoengine import Document, StringField, IntField, ReferenceField, ListField
from app.model.user import UserModel


class TagModel(Document):
    name = StringField(max_length=255, required=True)


class CommentModel(Document):
    content = StringField(max_length=255, required=True)
    like = IntField()
    author = ReferenceField(UserModel)
    next_comment = ListField(ReferenceField("self"))


class ColumnModel(Document):
    title = StringField(max_length=255, required=True)
    author = ReferenceField(UserModel)
    content = StringField()
    tags = ListField(ReferenceField(TagModel))
    comments = ListField(ReferenceField(CommentModel))


class BoardModel(Document):
    columns = ListField(ReferenceField(ColumnModel))
    name = StringField(max_length=255, required=True)
