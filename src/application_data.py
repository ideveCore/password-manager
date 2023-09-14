from __future__ import annotations
from typing import Optional, Union, Any, Dict, List

from .db import Database, Password_manager_query, Query_user_builder, User_db_item, Query_master_password_builder

class Application_data:
    instance = None
    _db: Database
    _user: Optional[User_db_item] = None
    _data: Dict = {}

    @staticmethod
    def new() -> Application_data:
        """Create a new instance of Application_data"""
        instnace = Application_data()
        instnace._db = Database()
        instnace._db.setup()

        return instnace

    @staticmethod
    def get() -> Application_data:
        if not Application_data.instance:
            Application_data.instance = Application_data.new()
        return Application_data.instance

    def get_user(self) -> Optional[User_db_item]:
        if not self._user:
            response = self._db.query(self._query_all_users())
            if response:
               self._user = response[0]
        return self._user

    def get_user_master_password(self, id: int) -> Optional[str]:
        if id:
            query = Query_master_password_builder.get(id)
            if query:
                response = self._db.query(query)
                if response:
                    return response[0].master_password

    def save_user(self, user: User_db_item) -> Optional[User_db_item]:
        if not user: return None
        self._user = None
        return self._db.save_user(user)

    def _query_all_users(self) -> Password_manager_query:
        query = Query_user_builder()
        query.get_all()
        return query.build()

