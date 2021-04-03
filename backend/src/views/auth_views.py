from flask import redirect, url_for, request, make_response, render_template, flash
from flask.views import MethodView
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from backend.src.auth import UserLogin
from backend.src.data.context import Context


class Login(MethodView):

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        user = Context.get_db_worker().get_user_by_name(request.form["name"])

        if user and check_password_hash(user.pass_hash, request.form["psw"]):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(request.args.get("next") or url_for("index"))
        return make_response(render_template("user_not_found.html"))

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for("index"))

        return make_response(render_template("login.html"))


class Logout(MethodView):

    @login_required
    def get(self):
        logout_user()
        flash("Вы вышли из аккаунта", "success")
        return redirect(url_for('logon'))
