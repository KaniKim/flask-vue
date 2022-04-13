from ..model.user_model import User
from ..model.post_model import Post
from ..model.post_model import Tag
from ..model.post_model import Category
from ..model.post_model import Comment
from ..model.user_model import User

import json
from bson.objectid import ObjectId

from abc import ABC, abstractmethod
from typing import Dict, List


class BasePostRepository(ABC):
    @abstractmethod
    def save_post(
        self,
        title: str,
        author: User,
        content: str,
        tags: List[str],
        comments: List[Comment],
        category: str,
    ):
        pass

    @abstractmethod
    def find_posts_by_category(self, category: str):
        pass

    @abstractmethod
    def find_post_by_obj(self, obj: ObjectId):
        pass


class PostRepository(BasePostRepository):
    def save_post(
        self,
        title: str,
        author: User,
        content: str,
        tags: List[str],
        comments: List[Comment],
        category: str,
    ) -> Dict:
        tag_mongo = [Tag(name=tag) for tag in tags]
        for tag in tag_mongo:
            tag.save()
        post_author = User.objects.filter(email=author).first()
        post = Post(
            title=title,
            author=post_author,
            content=content,
            tags=tag_mongo,
            comments=comments,
        )
        post.save()

        category_model = Category.objects.filter(name=category).first()

        if category_model is None:
            Category(
                name=category,
                posts=[post.to_dbref()],
            ).save()
        else:
            category_model.posts.append(post).save()

        return {
            "title": title,
            "author": post_author.name,
            "content": content,
            "tags": tags,
            "comments": [],
        }

    def find_posts_by_category(self, category: str):

        posts = Category.objects.filter(name=category)[0].posts
        posts_model = [Post.objects.filter(id=post.id).first() for post in posts]

        return [
            {
                "title": post.title,
                "author": json.loads(
                    User.objects.filter(id=post.author.id)[0].to_json()
                )["name"],
                "tags": [
                    json.loads(Tag.objects.filter(id=tag.id)[0].to_json())["name"]
                    for tag in post.tags
                ],
                "obj": str(post.id),
            }
            for post in posts_model
        ]

    def find_post_by_obj(self, obj: ObjectId):
        post_model = Post.objects.filter(id=obj).first()

        return json.loads(post_model.to_json())
