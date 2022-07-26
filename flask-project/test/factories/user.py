import factory
from factory import post_generation
from factory.fuzzy import FuzzyChoice
from factory.mongoengine import MongoEngineFactory

from app.model.user import UserModel

class UserFactory(MongoEngineFactory):
    class Meta:
        model = UserModel

    name = factory.Faker("name")
    email = factory.sequence(lambda n: f"{n}_" + factory.Faker("email").generate())

    @post_generation
    def post(self, create, extracted, **kwargs):
        if not create:
            return


    @classmethod
    def create_with_token(cls, **kwargs):
        pass
