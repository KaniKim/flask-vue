import datetime
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
        return UserFactory(
            password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        )

    class Describe_singup:
        @pytest.fixture
        def form(self):
            return {
                "email": "test@email.com",
                "name": Faker().name(),
                "password": Faker().password(
                    length=10,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True,
                ),
            }

        @pytest.fixture
        def subject(self, client, form):
            url = url_for("UserView:sign_up")
            return client.post(
                url, data=json.dumps(form), content_type="application/json"
            )

        class Context_정상_요청:
            def test_가입이_완료된다(self, subject):
                assert subject.status_code == 201

            @pytest.fixture
            def form(self):
                return {
                    "email": "test@email.com",
                    "name": Faker().name(),
                    "password": Faker().password(
                        length=10,
                        special_chars=True,
                        digits=True,
                        upper_case=True,
                        lower_case=True,
                    ),
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
            return client.post(
                url, data=json.dumps(form), content_type="application/json"
            )

        class Context_정상_요청:
            def test_로그인이_완료된다(self, subject):
                assert subject.status_code == 201

            def test_jwt_토큰이_정상_발급된다(self, subject, form):
                token = jwt.decode(
                    subject.json["access_token"],
                    algorithms="HS256",
                    options={"verify_signature": False},
                )

                assert token["sub"] == form["email"]
                assert token["exp"] - token["nbf"] == 60

                token = jwt.decode(
                    subject.json["refresh_token"],
                    algorithms="HS256",
                    options={"verify_signature": False},
                )

                assert token["sub"] == form["email"]
                assert token["exp"] - token["nbf"] == 1209600

        class Context_비밀번호가_틀린_요청:
            @pytest.fixture
            def form(self, create_user):
                return {
                    "email": create_user.email,
                    "password": "qwer1234!1",
                }

            def test_비밀번호가_틀린다(self, subject):
                assert subject.status_code == 409

        class Context_비밀번호와_이메일_틀린_요청:
            @pytest.fixture
            def form(self):
                return {
                    "email": Faker().company_email(),
                    "password": "qwer1234!1",
                }

            def test_이메일과_비밀번호_모두_틀린다(self, subject):
                assert subject.status_code == 404

    class Describe_me:
        @pytest.fixture
        def url(self):
            return url_for("UserView:index")

        @pytest.fixture
        def form_login(self, create_user, password):
            return {
                "email": create_user.email,
                "password": password,
            }

        @pytest.fixture
        def jwt(self, client, form_login):
            url = url_for("UserView:login")
            return client.post(
                url, data=json.dumps(form_login), content_type="application/json"
            )

        class Describe_get:
            @pytest.fixture
            def form(self, create_user, password):
                return {
                    "email": create_user.email,
                    "password": password,
                }

            @pytest.fixture
            def subject(self, jwt, client, url):
                access_token = jwt.json["access_token"]
                headers = {"Authorization": f"Bearer {access_token}"}
                return client.get(url, headers=headers, content_type="application/json")

            def test_올바른_토큰이면_자신의_정보를_받아온다(self, subject, create_user):
                assert subject.status_code == 200

                name = subject.json["name"]
                email = subject.json["email"]

                assert email == create_user.email
                assert name == create_user.name

        class Describe_put:
            @pytest.fixture
            def original_name(self, create_user):
                name = create_user.name
                return name

            @pytest.fixture
            def form(self, create_user, password):
                return {
                    "email": create_user.email,
                    "name": str(Faker().name()),
                    "password": password,
                }

            @pytest.fixture
            def subject(self, jwt, client, url, form):
                access_token = jwt.json["access_token"]
                headers = {"Authorization": f"Bearer {access_token}"}
                return client.put(
                    url,
                    data=json.dumps(form),
                    headers=headers,
                    content_type="application/json",
                )

            def test_올바른_토큰이면_자신의_이름을_수정한다(self, subject, create_user, original_name):
                assert subject.status_code == 201

                user = UserModel.objects.filter(email=create_user.email).first()
                name = user.name
                email = user.email

                assert email == create_user.email
                assert name != original_name

        class Describe_delete:
            @pytest.fixture
            def form(self, create_user, password):
                return {
                    "email": create_user.email,
                    "name": str(Faker().name()),
                    "password": password,
                }

            @pytest.fixture
            def subject(self, jwt, client, url, form):
                access_token = jwt.json["access_token"]
                headers = {"Authorization": f"Bearer {access_token}"}
                return client.delete(
                    url,
                    data=json.dumps(form),
                    headers=headers,
                    content_type="application/json",
                )

            def test_올바른_토큰이면_자신을_삭제한다(self, subject, create_user):
                assert subject.status_code == 204

                user = UserModel.objects.filter(email=create_user.email).first()
                email = user.email

                assert email == create_user.email
                assert user.deleted_at < datetime.datetime.now()
                assert user.activated == False
