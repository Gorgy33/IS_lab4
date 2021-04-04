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
        statement = "SELECT * FROM users WHERE login = %s;"
        params = [name]
        return self.db_connector.one_select_execute(statement, params)

    def get_user(self, user_id):
        statement = "SELECT id, login, role, nickname FROM users WHERE id = %s;"
        params = [user_id]
        return self.db_connector.one_select_execute(statement, params)

    def get_users(self):
        statement = "SELECT id, login, role, nickname FROM users;"
        return self.db_connector.all_select_execute(statement)

    def insert_user(self, name, password_hash, role, nickname):
        statement = 'INSERT INTO users VALUES (default, %s, %s, %s, %s);'
        params = [password_hash, name, role, nickname]
        return self.db_connector.insert_or_update_execute(statement, params)

    def get_notes(self):
        statement = "SELECT text, author, id FROM notes;"
        return self.db_connector.all_select_execute(statement)

    def insert_notes(self, text, author):
        statement = 'INSERT INTO notes VALUES (default, %s, %s);'
        params = [text, author]
        return self.db_connector.insert_or_update_execute(statement, params)

    def delete_note(self, note_id):
        statement = 'DELETE FROM notes WHERE id = %s'
        params = [note_id]
        return self.db_connector.insert_or_update_execute(statement, params)
