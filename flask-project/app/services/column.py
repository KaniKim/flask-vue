from typing import Optional, List

from app.model.column import ColumnModel, TagModel, BoardModel
from app.model.user import UserModel


class ColumnService:
    def __init__(self, title: Optional[str], content: Optional[str], tags: List[Optional[str]], email: Optional[str], name: Optional[str]):
        self.title = title
        self.content = content
        self.tags = tags
        self.email = email
        self.name = name

    def save_column(self):
        tag_models = [TagModel(name=tag).save() for tag in self.tags]
        column_model = ColumnModel(
            title = self.title,
            author = UserModel.objects.filter(email=self.email).first(),
            tags = tag_models,
            content = self.content
        )
        column_model.save()

        board_model = BoardModel.objects(name=self.name).first()

        if board_model:
            board_model.columns.append(column_model)
            board_model.save()
        else:
            board_model = BoardModel(name=self.name, columns=[])
            board_model.columns.append(column_model)
            board_model.save()

        return True
