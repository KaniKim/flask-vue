from ..model.user_model import User as UserMongo
from abc import ABC, abstractmethod
from typing import Dict, Optional

import json


class BaseUserRepository(ABC):
    @abstractmethod
    def save_user(self, name: str, email: str, password: str) -> Dict:
        pass

    @abstractmethod
    def find_user_by_email(self, email: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def find_user_by_email_and_password(
        self, email: str, password: str
    ) -> Optional[Dict]:
        pass


class UserRepository(BaseUserRepository):
    def save_user(self, name: str, email: str, password: str) -> Dict:

        UserMongo(name=name, email=email, password=password, activated=True).save()

        return {"name": name, "email": email, "activated": True}

    def find_user_by_email(self, email: str) -> Optional[Dict]:
        user_mongo = UserMongo.objects.filter(email=email)

        if len(user_mongo) == 0:
            return None

        return json.loads(user_mongo.to_json())

    def find_user_by_email_and_password(
        self, email: str, password: str
    ) -> Optional[Dict]:
        user_mongo = UserMongo.objects.filter(email=email, password=password)

        if len(user_mongo) == 0:
            return None

        return json.loads(user_mongo.to_json())
