import logging

from flask import make_response, render_template, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from backend.src.auth import roles_restriction
from backend.src.data.context import Context
from backend.src.views.schemas import CreateUserInputSchema


class GetUsers(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def get(self):
        users = Context.get_db_worker().get_users()
        items = [{"login": user.login, "role": user.role, "nickname": user.nickname} for user in users]
        return make_response(render_template("users.html", items=items, role=current_user.get_role()))


class AddUser(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def get(self):
        return make_response(render_template("add_user.html", role=current_user.get_role()))

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def post(self):
        data = {
            'name': request.form["name"],
            'password': request.form["password"],
            'role': request.form["role"],
            'nickname': request.form["nickname"],
        }
        errors = CreateUserInputSchema().validate(data)
        if errors:
            flash(errors, category='error')
            return redirect(url_for("users"))
        try:
            Context.get_db_worker().insert_user(
                data["name"],
                generate_password_hash(data["password"]),
                data["role"],
                data["nickname"],
            )
        except Exception as error:
            logging.exception(error)
            flash('Something going wrong, sorry')
        return redirect(url_for("users"))
