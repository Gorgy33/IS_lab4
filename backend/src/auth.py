import functools

from flask import make_response
from flask_login import UserMixin
from flask_login import current_user


class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)

    def get_role(self):
        return str(self.__user.role)


def roles_restriction(roles):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.get_role() in roles:
                return f(*args, **kwargs)
            return make_response("Not Found", 404)
        return wrapper
    return decorator
