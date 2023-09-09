from __future__ import annotations
from typing import Optional, Union, Any, Dict, List

import gi
gi.require_version('Gda', '6.0') 
from gi.repository.Gda import Config, Connection, SqlBuilder, SqlOperatorType, SqlStatementType, Statement, StatementSqlFlag
from gi.repository.Gio import Settings
from gi.repository import GLib

class User_db_item:
    def __init__(self, id: Union[int, None], first_name: str, last_name: str, username: str, email: str, master_password: str, master_password_tip: str, timestamp: int):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.master_password = master_password
        self.master_password_tip = master_password_tip
        self.timestamp = timestamp

class Password_manager_query:
    statement: Statement = None
    def __init__(self, statement: Statement):
        self.statement = statement

def add_expr_value(builder: SqlBuilder, value: Any) -> float:
    return builder.add_expr_value(value)

# =====================
# QUERY get users
# ====================
class Query_user_builder:
    _builder: SqlBuilder
    _conditions: List[float]
    def __init__(self) -> None:
        self._conditions = [];
        self._builder = SqlBuilder.new(
            stmt_type = SqlStatementType.SELECT,    
        )
        self._builder.select_add_field('id', 'user', 'id')
        self._builder.select_add_field('first_name', 'user', 'first_name')
        self._builder.select_add_field('last_name', 'user', 'last_name')
        self._builder.select_add_field('username', 'user', 'username')
        self._builder.select_add_field('email', 'user', 'email')
        self._builder.select_add_field('master_password', 'user', 'master_password')
        self._builder.select_add_field('master_password_tip', 'user', 'master_password_tip')
        self._builder.select_add_field('timestamp', 'user', 'timestamp')
        self._builder.select_add_target('user', None)

    def get_all(self):
        return self

    def with_id(self, id=None):
        if id is not None:
            return self._conditions.append(
                self._builder.add_cond(
                    SqlOperatorType.EQ,
                    self._builder.add_field_id('id', 'user'),
                    add_expr_value(self._builder, id),
                    0,
                )
            )
        return self

    def build(self) -> Password_manager_query:
        if len(self._conditions) > 0:
            self._builder.set_where(self._builder.add_cond_v(SqlOperatorType.AND, self._conditions))
        return Password_manager_query(self._builder.get_statement())



class Query_builder:
    _builder: SqlBuilder
    _conditions: List[float]
    def __init__(self):
        self._conditions = [];
        self._builder = SqlBuilder.new(
            stmt_type = SqlStatementType.SELECT,    
        )
        self._builder.select_add_field('id', 'user', 'id')
        self._builder.select_add_field('name', 'user', 'name')
        self._builder.select_add_field('master_password', 'user', 'master_password')

        self._builder.select_add_target('user', None)

    def get_all(self):
        print(self._builder.get_statement())
        return self

    def with_id(self, id=None):
        if id is not None:
            return self._conditions.append(
                self._builder.add_cond(
                    SqlOperatorType.EQ,
                    self._builder.add_field_id('id', 'user'),
                    add_expr_value(self._builder, id),
                    0,
                )
            )
        return self

    def build(self) -> Password_manager_query:
        if len(self._conditions) > 0:
            self._builder.set_where(self._builder.add_cond_v(SqlOperatorType.AND, self._conditions))
        return Password_manager_query(self._builder.get_statement())


class Database():
    _connection: Connection = None
    def __init__(self):
        self.data_dir = GLib.get_user_config_dir();
        self._connection = Connection(
            provider = Config.get_provider('SQLite'),
            cnc_string = f'DB_DIR={self.data_dir};DB_NAME=passwordmanager',
        )
        self._connection.open()
    def setup(self):
        if not self._connection.is_opened(): return
        
        self._connection.execute_non_select_command(
            """
                create table if not exists user
                (
                    id INTEGER NOT NULL CONSTRAINT user_pk PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    master_password TEXT NOT NULL,
                    master_password_tip TEXT NOT NULL,
                    timestamp INTEGER NOT NULL
                )
            """
        )
        # self._connection.execute_non_select_command(
        #     """
        #         create table if not exists salts
        #         (
        #             id INTEGER NOT NULL CONSTRAINT user_pk PRIMARY KEY AUTOINCREMENT,
        #             salt TEXT UNIQUE NOT NULL
        #             user_id INTERGER
        #         )
        #     """
        # )

        self._connection.execute_non_select_command("""
            create unique index if not exists user_id_uindex on user (id);
        """);
    def save_user(self, db_item: User_db_item) -> Optional[User_db_item]:
        if not self._connection.is_opened(): return None
        
        builder = SqlBuilder.new(
            stmt_type = SqlStatementType.INSERT
        )
        builder.set_table('user')
        builder.add_field_value_as_gvalue('first_name', db_item.first_name)
        builder.add_field_value_as_gvalue('last_name', db_item.last_name)
        builder.add_field_value_as_gvalue('username', db_item.username)
        builder.add_field_value_as_gvalue('email', db_item.email)
        builder.add_field_value_as_gvalue('master_password', db_item.master_password)
        builder.add_field_value_as_gvalue('master_password_tip', db_item.master_password_tip)
        builder.add_field_value_as_gvalue('timestamp', db_item.timestamp)
        _, row = self._connection.statement_execute_non_select(builder.get_statement(), None);
        id = row.get_nth_holder(0).get_value();
        if not id:
            return None;

        item = User_db_item(
                id=id,
                first_name=db_item.first_name,
                last_name=db_item.last_name,
                username=db_item.username,
                email=db_item.email,
                master_password=db_item.master_password,
                master_password_tip=db_item.master_password_tip,
                timestamp=db_item.timestamp,
            )
        return item

    def delete(self, id: int) -> None:
        if not self._connection.is_opened(): return None
        builder = SqlBuilder.new(
            stmt_type = SqlStatementType.DELETE
        )

        builder.set_table('user')
        builder.set_where(
            builder.add_cond(SqlOperatorType.EQ, builder.add_field_id('id', 'user'), add_expr_value(builder, id), 0),
        )
        self._connection.statement_execute_non_select(builder.get_statement(), None)

    def query(self, password_manager_query: Password_manager_query) -> Union[List[Db_item], None]:
        if not self._connection.is_opened(): return None
        # print(f'{password_manager_query.statement.to_sql_extended(self._connection, None, StatementSqlFlag.PRETTY)}');
        dm = self._connection.statement_execute_select(password_manager_query.statement, None)
        iter = dm.create_iter()
        itemList = []

        while (iter.move_next()):
            id = iter.get_value_for_field('id')
            first_name  = iter.get_value_for_field('first_name')
            last_name = iter.get_value_for_field('last_name')
            username = iter.get_value_for_field('username')
            email  = iter.get_value_for_field('email')
            master_password = iter.get_value_for_field('master_password')
            master_password_tip = iter.get_value_for_field('master_password_tip')
            timestamp = iter.get_value_for_field('timestamp')


            itemList.append(User_db_item(
                id=id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                master_password=master_password,
                master_password_tip=master_password_tip,
                timestamp=timestamp,
            ))

        return itemList

