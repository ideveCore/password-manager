from __future__ import annotations
from typing import Optional, Union, Any, Dict, List

from .db import Database, Query_builder, Password_manager_query, Query_user_builder, User_db_item

class Application_data:
    def __init__(self):
        self._db = Database()
        self._user: Optional[List[User_db_item]] = [];
        self._data: Dict = {}


    def setup(self) -> Application_data:
        self._db.setup()
        return self

    def get_user(self) -> Optional[List[User_db_item]]:
        if not self._user: 
            self._user = self._db.query(self._query_all_users());
        return self._user

    def save_user(self, user: User_db_item) -> Optional[User_db_item]:
        if not user: return None
        self._user = []
        return self._db.save_user(user)

    def _query_all_users(self) -> Password_manager_query:
        query = Query_user_builder()
        query.get_all()
        return query.build()
