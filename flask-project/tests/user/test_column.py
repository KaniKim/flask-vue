import json

import bcrypt
import pytest
from bson import ObjectId
from flask import url_for

from app.model.column import ColumnModel, CommentModel
from app.model.user import UserModel
from tests.factories.column import ColumnFactory
from tests.factories.user import UserFactory


class Describe_ColumnView:
    @pytest.fixture
    def password(self):
        return "qwer1234!"

    @pytest.fixture
    def create_user(self, password):
        return UserFactory(
            password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        )

    @pytest.fixture
    def login(self, create_user, password, client):
        url = url_for("UserView:login")
        return client.post(
            url,
            data=json.dumps({"email": create_user.email, "password": password}),
            content_type="application/json",
        )

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
