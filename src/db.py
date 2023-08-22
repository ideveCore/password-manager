from __future__ import annotations
from typing import Optional, Union, Any, Dict, List

import gi
gi.require_version('Gda', '6.0') 
from gi.repository.Gda import Config, Connection, SqlBuilder, SqlOperatorType, SqlStatementType, Statement, StatementSqlFlag
from gi.repository.Gio import Settings
from gi.repository import GLib

class Db_item:
    def __init__(self, id: Union[int, None], name: str, master_password: str):
        self.id = id
        self.name = name
        self.master_password = master_password

class Password_manager_query:
    statement: Statement = None
    def __init__(self, statement: Statement):
        self.statement = statement

def add_expr_value(builder: SqlBuilder, value: Any) -> float:
    return builder.add_expr_value(value)

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


class Gda_setup():
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
                    id integer not null constraint clipboard_pk primary key autoincrement,
                    name text not null,
                    master_password text not null
                )
            """
        )
    def save(self, db_item: Db_item) -> Optional[Db_item]:
        if not self._connection.is_opened(): return None
        
        builder = SqlBuilder.new(
            stmt_type = SqlStatementType.INSERT
        )
        builder.set_table('user')
        builder.add_field_value_as_gvalue('name', db_item.name)
        builder.add_field_value_as_gvalue('master_password', db_item.master_password)
        _, row = self._connection.statement_execute_non_select(builder.get_statement(), None);
        id = row.get_nth_holder(0).get_value();
        print('id', id)
        if not id:
            return None;

        item = Db_item(id = id, name = db_item.name, master_password=db_item.master_password)
        
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
            name  = iter.get_value_for_field('name')
            master_password = iter.get_value_for_field('master_password')

            itemList.append(Db_item(id=id, name=name, master_password=master_password))

        return itemList

