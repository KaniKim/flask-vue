import json
import bcrypt

import jwt
import pytest

from faker import Faker
from flask import url_for

from app.model.user import UserModel
from tests.factories.user import UserFactory


class Describe_UserView:
    @pytest.fixture
    def password(self):
        return "qwer1234!"

    @pytest.fixture
    def create_user(self, password):
        return UserFactory(password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()))

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

    class Describe_login:
        @pytest.fixture
        def form(self, create_user, password):
            return {
                "email": create_user.email,
                "password": password,
            }

        @pytest.fixture
        def subject(self, client, form):
            url = url_for("UserView:login")
            return client.post(url, data=json.dumps(form), content_type="application/json")

        class Context_정상_요청:
            def test_로그인이_완료된다(self, subject):
                assert subject.status_code == 201

            def test_jwt_토큰이_정상_발급된다(self, subject, form):
                token = jwt.decode(subject.json["access_token"], algorithms="HS256", options={"verify_signature": False})

                assert token["sub"] == form["email"]
                assert token["exp"] - token["nbf"] == 60


