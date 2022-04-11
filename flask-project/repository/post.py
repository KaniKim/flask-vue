from ..model.user_model import User
from ..model.post_model import Post
from ..model.post_model import Tag
from ..model.post_model import Category
from ..model.post_model import Comment
from ..model.user_model import User

import json

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

        Post(
            title=title,
            author=author,
            content=content,
            tags=tag_mongo,
            comments=comments,
        ).save()

        Category(
            name=category,
            posts=[
                Post(
                    title=title,
                    author=author,
                    content=content,
                    tags=tag_mongo,
                    comments=comments,
                ).save()
            ],
        ).save()

        return {
            "title": title,
            "author": User.name,
            "content": content,
            "tags": tags,
            "comments": [],
        }

    def find_posts_by_category(self, category: str):
        posts = Category.objects.filter(name=category)[0].posts
        posts_model = [Post.objects.filter(id=post.id)[0] for post in posts]

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
            }
            for post in posts_model
        ]
