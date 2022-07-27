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
    password = Faker().password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

