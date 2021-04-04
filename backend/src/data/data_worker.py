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

    @staticmethod
    def get_instance(*args):
        if not DataWorker.__instance__:
            DataWorker(*args)
        return DataWorker.__instance__

    def get_user_by_name(self, name):
        return self.db_connector.one_select_execute(f"SELECT * FROM users WHERE name = '{name}';")

    def get_user(self, user_id):
        return self.db_connector.one_select_execute(f"SELECT id, name, role FROM users WHERE id = '{user_id}';")

    def get_users(self):
        return self.db_connector.all_select_execute("SELECT id, name, role FROM users;")

    def insert_user(self, name, password_hash, role):
        return self.db_connector.insert_or_update_execute(
            f"INSERT INTO users VALUES (default, '{password_hash}', '{name}', '{role}');")
