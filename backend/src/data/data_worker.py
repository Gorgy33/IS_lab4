from backend.src.data.db_connector import DBConnector


class DataWorker:
    __instance__ = None

    def __init__(self, config):
        if self.__instance__ is not None:
            raise Exception("Can't create other instance")
        self.db_connector = DBConnector(config)
        DataWorker.__instance__ = self

    def get_secret_key(self):
        return self.db_connector.get_common_data(field="SECRET_KEY").value

    def get_data_pusher_token(self):
        return self.db_connector.get_common_data(field="DATA_PUSHER_TOKEN").value

    @staticmethod
    def get_instance(*args):
        if not DataWorker.__instance__:
            DataWorker(*args)
        return DataWorker.__instance__

    def get_user_by_name(self, name):
        return self.db_connector.one_select_execute(f"SELECT * FROM users WHERE name = '{name}';")
