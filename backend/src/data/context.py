from backend.src.data.data_worker import DataWorker


class Context:

    __instance__ = None

    db_connector = None

    config = {}

    def __init__(self, config):
        if self.__instance__ is not None:
            raise Exception("Can't create other instance")
        Context.config = config
        Context.__instance__ = self
        Context.db_connector = DataWorker.get_instance(config)

    @staticmethod
    def get_instance(*args):
        if not Context.__instance__:
            Context(*args)
        return Context.__instance__

    @staticmethod
    def get_db_worker() -> DataWorker:
        return Context.db_connector


def get_context() -> Context:
    return Context.get_instance()
