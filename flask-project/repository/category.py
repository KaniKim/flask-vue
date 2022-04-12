from abc import ABC, abstractmethod
from typing import Dict, List

import json

from ..model.post_model import Category


class BaseCategoryRepository(ABC):
    @abstractmethod
    def find_all_category(self) -> List[Dict]:
        pass


class CategoryRepository(BaseCategoryRepository):
    def find_all_category(self) -> List[Dict]:
        return [
            json.loads(category.to_json())["name"] for category in Category.objects()
        ]
