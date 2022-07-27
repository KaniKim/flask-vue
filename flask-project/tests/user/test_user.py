import json
import pytest

from faker import Faker
from flask import url_for

from app.model.user import UserModel
from tests.factories.user import UserFactory


class Describe_UserView:
    @pytest.fixture
    def create_user(self):
        return UserFactory.create()

    class Describe_singup:
        @pytest.fixture
        def form(self):
            return {
                "email": "test@email.com",
                "name": Faker().name(),
                "password": Faker().password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
            }

        @pytest.fixture
        def subject(self, client, form):
            url = url_for("UserView:sign_up")
            return client.post(url, data=json.dumps(form), content_type="application/json")

        class Context_정상_요청:
            def test_가입이_완료된다(self, subject):
                assert subject.status_code == 201
                assert UserModel.objects().count() == 1

            @pytest.fixture
            def form(self):
                return {
                    "email": "test@email.com",
                    "name": Faker().name(),
                    "password": Faker().password(length=10, special_chars=True, digits=True, upper_case=True,
                                                 lower_case=True)
                }

            class Context_비정상_요청:
                def test_같은_이메일은_중복_가입이_안된다(self, subject):
                    assert subject.status_code == 409



