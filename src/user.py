from __future__ import annotations
from typing import Optional, Union, Any, Dict, List
from .db import User_db_item
from .application_data import Application_data as data


class User:
    instance: Union[User, None] = None
    _data: Union[User_db_item, None] = None

    @staticmethod
    def new() -> User:
        instance = User()
        instance.data = data.get().get_user()
        return instance

    @staticmethod
    def get() -> User:
        if not User.instance:
            User.instance = User.new()
        return User.instance

    @property
    def data(self) -> Union[User_db_item, None]:
        return self._data

    @data.setter
    def data(self, data: Union[User_db_item, None]):
        self._data = data

