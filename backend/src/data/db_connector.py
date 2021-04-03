import logging

import pg_simple
from pg_simple import ThreadedConnectionPool


class DBConnector:
    __instance__ = None
    try_connect_count = 5

    def __init__(self, db_config):
        if self.__instance__ is not None:
            raise Exception("Can't create other instance")
        self.connection_pool = pg_simple.config_pool(
            max_conn=250, expiration=60, pool_manager=ThreadedConnectionPool, dsn=db_config["db_connection_string"])
        self.config = db_config
        self.__instance__ = self

    def execute_query(self, query: str, return_value=True) -> list:
        logging.info(query)
        try:
            with pg_simple.PgSimple(self.connection_pool) as _db:
                execute = _db.execute(query)
                _db.commit()
                if return_value:
                    return execute.fetchall()
        except Exception as error:
            logging.error(query)
            logging.exception(error)
        return []

    @staticmethod
    def get_instance(*args):
        if not DBConnector.__instance__:
            DBConnector(*args)
        return DBConnector.__instance__

    def all_select_execute(self, query):
        return self.execute_query(query)

    def one_select_execute(self, query):
        result = self.execute_query(query)
        if len(result) == 0:
            return None
        return result[0]

    def insert_or_update_execute(self, query):
        self.execute_query(query, return_value=False)
        return "Ok"

    def get_common_data(self, field):
        return self.one_select_execute(f'SELECT value FROM common WHERE "field" = "{field}";')
