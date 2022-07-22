from typing import Optional, List

from app.model.column import ColumnModel, TagModel
from app.model.user import UserModel


class ColumnService:
    def __init__(self, title: Optional[str], content: Optional[str], tags: List[Optional[str]], email: Optional[str]):
        self.title = title
        self.content = content
        self.tags = tags
        self.email = email

    def save_column(self):
        print(self.tags)
        tag_models = [TagModel(name=tag).save() for tag in self.tags]
        print(tag_models)
        column_model = ColumnModel(
            title = self.title,
            author = UserModel.objects.filter(email=self.email).first(),
            tags = tag_models,
            content = self.content
        )

        column_model.save()

        return True
