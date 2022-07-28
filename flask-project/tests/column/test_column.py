import json

import bcrypt
import pytest
from bson import ObjectId
from faker import Faker
from flask import url_for

from app.model.column import ColumnModel, CommentModel
from tests.factories.column import ColumnFactory
from tests.factories.user import UserFactory


class Describe_ColumnView:
    @pytest.fixture
    def password(self):
        return "qwer1234!"

    @pytest.fixture
    def create_user(self, password):
        return UserFactory(
            email = Faker().company_email(),
            password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        )

    @pytest.fixture
    def user_name(self, create_user):
        user = create_user.name
        return user

    @pytest.fixture
    def login(self, create_user, password, client):
        url = url_for("UserView:login")
        return client.post(
            url,
            data=json.dumps({"email": create_user.email, "password": password}),
            content_type="application/json",
        )

    class Describe_board:
        @pytest.fixture
        def subject(self, client, login):
            access_token = login.json["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            url = url_for("BoardView:index")
            return client.get(
                url,
                headers=headers,
                content_type="application/json",
            )

        def test_아무것도_없는_글_목록이_반환된다(self, subject):
            assert subject.status_code == 200
            assert subject.json["columns"] == []

        class Describe_post:
            @pytest.fixture
            def form(self):
                return {
                    "title": "hello",
                    "content": "nice",
                    "tags": ["to", "meet"],
                    "name": "you",
                }

            @pytest.fixture
            def subject(self, client, form, login):
                access_token = login.json["access_token"]
                headers = {"Authorization": f"Bearer {access_token}"}
                url = url_for("ColumnView:write_column")
                return client.post(
                    url,
                    data=json.dumps(form),
                    headers=headers,
                    content_type="application/json",
                )

            def test_Column에_제대로_저장된다(self, subject, form):
                assert subject.status_code == 201
                assert ColumnModel.objects().count() == 1

                column = ColumnModel.objects().first()

                assert column.title == form["title"]
                assert column.content == form["content"]
                assert len(column.tags) == 2

            @pytest.fixture
            def create_column(self, create_user):
                return ColumnFactory(author=create_user)

            @pytest.fixture
            def column_id(self, create_column):
                return create_column.id

            class Describe_column_all:
                @pytest.fixture
                def forms(self):
                    return [{
                        "title": "hello",
                        "content": "nice",
                        "tags": ["to", "meet"],
                        "name": "me",
                    }, {
                        "title": "hello",
                        "content": "nice",
                        "tags": ["to", "meet"],
                        "name": "good"
                    },]

                @pytest.fixture
                def subject_add_column(self, client, forms, login):
                    access_token = login.json["access_token"]
                    headers = {"Authorization": f"Bearer {access_token}"}
                    url = url_for("ColumnView:write_column")
                    return [client.post(
                        url,
                        data=json.dumps(form),
                        headers=headers,
                        content_type="application/json",
                    ) for form in forms]

                @pytest.fixture
                def subject(self, client, login, subject_add_column):
                    access_token = login.json["access_token"]
                    headers = {"Authorization": f"Bearer {access_token}"}
                    url = url_for("BoardView:index")
                    return client.get(
                        url,
                        headers=headers,
                        content_type="application/json",
                    )

                def test_모든_글이_조회된다(self, subject):
                    columns = subject.json["columns"]
                    assert subject.status_code == 200
                    assert len(columns) == 3

                    for col, name in zip(columns, ("you", "me", "good",)):
                        assert col["column"]["title"] == "hello"
                        assert col["column"]["content"] == "nice"
                        assert len(col["column"]["tags"]) == 2
                        assert col["name"] == name


            class Describe_like_post:
                @pytest.fixture
                def subject(self, client, column_id, login):
                    access_token = login.json["access_token"]
                    headers = {"Authorization": f"Bearer {access_token}"}
                    url = url_for("ColumnView:like_column", column_id=column_id)
                    return client.post(
                        url, headers=headers, content_type="application/json"
                    )

                def test_Column에_좋아요가_추가된다(self, subject, column_id):
                    assert subject.status_code == 201

                    column = ColumnModel.objects(id=ObjectId(column_id)).first()

                    assert column.like == 1

            class Describe_comment_post:
                @pytest.fixture
                def form(self):
                    return {"content": "Nice to meet you"}

                @pytest.fixture
                def subject(self, client, form, column_id, login):
                    access_token = login.json["access_token"]
                    headers = {"Authorization": f"Bearer {access_token}"}
                    url = url_for("ColumnView:post_comment_column", column_id=column_id)
                    return client.post(
                        url,
                        data=json.dumps(form),
                        headers=headers,
                        content_type="application/json",
                    )

                def test_Column에_댓글이_추가된다(self, subject, column_id):
                    assert subject.status_code == 201

                    column = ColumnModel.objects(id=ObjectId(column_id)).first()
                    assert len(column.comments) == 1

                    comment = CommentModel.objects(
                        id=ObjectId(column.comments[0].id)
                    ).first()
                    assert comment.content == "Nice to meet you"

                class Describe_comment_next_post:
                    @pytest.fixture
                    def form_comment(self):
                        return {"content": "Nice to meet you"}

                    @pytest.fixture
                    def subject_comment(self, client, form_comment, column_id, login):
                        access_token = login.json["access_token"]
                        headers = {"Authorization": f"Bearer {access_token}"}
                        url = url_for("ColumnView:post_comment_column", column_id=column_id)
                        return client.post(
                            url,
                            data=json.dumps(form_comment),
                            headers=headers,
                            content_type="application/json",
                        )

                    @pytest.fixture
                    def comment_id(self, column_id, subject_comment):
                        column = ColumnModel.objects(id=ObjectId(column_id)).first()
                        comment = CommentModel.objects(
                            id=ObjectId(column.comments[0].id)
                        ).first()
                        return comment.id

                    @pytest.fixture
                    def form(self):
                        return {"content": "Nice to meet you too"}

                    @pytest.fixture
                    def subject(self, client, form, comment_id, login):
                        access_token = login.json["access_token"]
                        headers = {"Authorization": f"Bearer {access_token}"}
                        url = url_for("CommentView:comment_next", comment_id=comment_id)
                        return client.post(
                            url,
                            data=json.dumps(form),
                            headers=headers,
                            content_type="application/json",
                        )

                    def test_Comment에_대댓글이_추가된다(self, subject, comment_id):
                        assert subject.status_code == 201

                        comment = CommentModel.objects(id=ObjectId(comment_id)).first()
                        assert len(comment.next_comment) == 1
                        next_comment = CommentModel.objects(
                            id=ObjectId(comment.next_comment[0].id)
                        ).first()
                        assert next_comment.content == "Nice to meet you too"

                    class Describe_get_comment_all:
                        @pytest.fixture
                        def form_comment(self):
                            return {"content": "Nice to meet you"}

                        @pytest.fixture
                        def subject_comment(self, client, form_comment, column_id, login):
                            access_token = login.json["access_token"]
                            headers = {"Authorization": f"Bearer {access_token}"}
                            url = url_for("ColumnView:post_comment_column", column_id=column_id)
                            return client.post(
                                url,
                                data=json.dumps(form_comment),
                                headers=headers,
                                content_type="application/json",
                            )

                        @pytest.fixture
                        def comment_id(self, column_id, subject_comment):
                            column = ColumnModel.objects(id=ObjectId(column_id)).first()
                            comment = CommentModel.objects(
                                id=ObjectId(column.comments[0].id)
                            ).first()
                            return comment.id

                        @pytest.fixture
                        def form_next(self):
                            return {"content": "Nice to meet you too"}

                        @pytest.fixture
                        def subject_next(self, client, form_next, comment_id, login):
                            access_token = login.json["access_token"]
                            headers = {"Authorization": f"Bearer {access_token}"}
                            url = url_for("CommentView:comment_next", comment_id=comment_id)
                            return client.post(
                                url,
                                data=json.dumps(form_next),
                                headers=headers,
                                content_type="application/json",
                            )

                        @pytest.fixture
                        def subject(self, client, login, column_id, subject_next):
                            access_token = login.json["access_token"]
                            headers = {"Authorization": f"Bearer {access_token}"}
                            url = url_for("ColumnView:get_comment_column", column_id=column_id)
                            return client.get(url, headers=headers, content_type="application/json")

                        def test_Column에_지금까지_쓴_댓글_및_작성자를_불러온다(self, subject, user_name):
                            assert subject.status_code == 200

                            comment = subject.json["comments"][0]
                            assert comment["content"] == "Nice to meet you"
                            assert comment["author"] == user_name

                            next_comment = comment["next_comment"][0]
                            assert next_comment["content"] == "Nice to meet you too"
                            assert next_comment["author"] == user_name

