import datetime

import factory
from factory.mongoengine import MongoEngineFactory
from faker import Faker
from app.model.user import UserModel

Faker.seed(str(datetime.datetime.now()))

class UserFactory(MongoEngineFactory):
    class Meta:
        model = UserModel

    name = factory.Faker("name")
    email = Faker().company_email()
    password = factory.LazyAttribute(lambda obj: obj.password)