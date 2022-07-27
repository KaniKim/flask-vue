import datetime

import factory
from factory.mongoengine import MongoEngineFactory
from faker import Faker

from app.model.user import UserModel
from tests.factories.user import UserFactory
from app.model.column import ColumnModel, CommentModel, TagModel, BoardModel

Faker.seed(str(datetime.datetime.now()))


class TagFactory(MongoEngineFactory):
    class Meta:
        model = TagModel

    name = Faker().name()


class CommentFactory(MongoEngineFactory):
    class Meta:
        model = CommentModel

    class Params:
        author = factory.SubFactory(UserModel)

    content = Faker().sentences()
    like = 0
    next_comment = factory.List(
        [factory.SubFactory("test.factories.column.CommentFactory") for _ in range(5)]
    )
    author = factory.SubFactory(UserFactory, author=factory.SelfAttribute("author"))


class ColumnFactory(MongoEngineFactory):
    class Meta:
        model = ColumnModel

    class Params:
        author = factory.SubFactory(UserModel)

    title = str(Faker().sentences())
    content = str(Faker().text())
    like = 0
    author = factory.SubFactory(UserFactory, author=factory.SelfAttribute("author"))


class BoardFactory(MongoEngineFactory):
    class Meta:
        model = BoardModel

    columns = factory.List([factory.SubFactory(ColumnFactory)])
    name = Faker().name()
