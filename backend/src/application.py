import logging

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from backend.src.auth import UserLogin
from backend.src.data.context import Context
from backend.src.urls import link_urls


def start_application(config):
    logger = logging.getLogger('authomatic.core')
    logger.addHandler(logging.StreamHandler())

    # init singletone database worker
    Context.get_instance(config)

    app = Flask("is_lab4", template_folder=config["path_to_template"], static_folder=config["path_to_static"])
    CORS(app)

    app.config["SECRET_KEY"] = Context.get_db_worker().get_secret_key()

    login_manager = LoginManager(app)
    login_manager.login_view = '/'
    login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
    login_manager.login_message_category = "success"

    @login_manager.user_loader
    def load_user(user_id):
        return UserLogin().fromDB(user_id, Context.get_db_worker())

    link_urls(app)
    app.run(config["host"], config["port"])
