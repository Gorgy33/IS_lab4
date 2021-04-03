from backend.src.data.data_worker import DataWorker


class Context:

    salt = 1234213423749812
    id_shift = 1000000000000000
    __instance__ = None

    db_connector = None

    pusher_secret_key = None

    config = {}

    def __init__(self, config):
        if self.__instance__ is not None:
            raise Exception("Can't create other instance")
        Context.config = config
        Context.__instance__ = self
        Context.db_connector = DataWorker.get_instance(config)
        Context.pusher_secret_key = Context.db_connector.get_data_pusher_token()

    @staticmethod
    def get_instance(*args):
        if not Context.__instance__:
            Context(*args)
        return Context.__instance__

    @staticmethod
    def get_db_worker() -> DataWorker:
        return Context.db_connector

    @staticmethod
    def get_pusher_key():
        return Context.pusher_secret_key


def get_context() -> Context:
    return Context.get_instance()
