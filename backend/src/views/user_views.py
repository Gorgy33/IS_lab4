import logging

from flask import make_response, render_template, request, flash, redirect, url_for, jsonify
from flask.views import MethodView
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from backend.src.auth import roles_restriction
from backend.src.data.context import Context
from backend.src.utils import hash_id, rehash_id


class GetUsers(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def get(self):
        users = Context.get_db_worker().get_users()
        items = [{"name": user.name, "role": Context.role_map[user.role], "id": hash_id(user.id)} for user in users]
        return make_response(render_template("users.html", items=items, role=current_user.get_role()))


class SaveUser(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def post(self):

        try:
            save_type = request.form["save_type"]

            name = request.form["name"]
            psw_hash = generate_password_hash(request.form["psw"])
            role = request.form["role"]

            if save_type == "save_user":
                user = request.form.get("id", None)
                if user is None:
                    flash("Ошибка при сохранении информации о пользователе")
                    return redirect(url_for("index"))
                state = request.form["state"]
                real_role = "DISABLE" if state == "off" else role

                if Context.get_db_worker().update_user(user, name, psw_hash, real_role) == "Ok":
                    flash("Успешно сохранено")
                    return redirect(url_for("users"))

            if Context.get_db_worker().insert_user(name, psw_hash, role) == "Ok":
                flash("Успешно сохранено")
                return redirect(url_for("users"))
            else:
                raise Exception("Can't save user")

        except Exception as error:
            logging.error(error)

        flash("Не удалось сохранить")
        return redirect(url_for("users"))


class AddUser(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def get(self):
        return make_response(render_template("add_user.html", role=current_user.get_role()))


class CreateUser(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def post(self):
        # check_psw_size(request.args["psw"])
        # check_unique_name(request.args["name"])
        # check_been_role(request.args["role"])

        try:
            return jsonify({"status": Context.get_db_worker().insert_user(
                request.args["name"],
                generate_password_hash(request.args["psw"]),
                request.args["role"]
            )})
        except Exception as error:
            logging.exception(error)
            return jsonify({"status": "Fail"})


class UserActions(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def get(self, user):
        user = rehash_id(int(user))
        user_info = Context.get_db_worker().get_user(user)
        info = {
            "name": user_info.name,
            "role": user_info.role
        }
        actions = Context.get_db_worker().select_user_actions(user)
        return make_response(render_template("user_actions.html", user=info, actions=actions,
                                             role=current_user.get_role()))
