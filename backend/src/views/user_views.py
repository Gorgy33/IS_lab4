import logging

from flask import make_response, render_template, request, jsonify
from flask.views import MethodView
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from backend.src.auth import roles_restriction
from backend.src.data.context import Context
from backend.src.utils import hash_id
from backend.src.views.schemas import CreateUserInputSchema


class GetUsers(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def get(self):
        users = Context.get_db_worker().get_users()
        items = [{"name": user.name, "role": user.role, "id": hash_id(user.id)} for user in users]
        return make_response(render_template("users.html", items=items, role=current_user.get_role()))


class AddUser(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def get(self):
        return make_response(render_template("add_user.html", role=current_user.get_role()))


class CreateUser(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN"])
    def post(self):
        data = request.args
        errors = CreateUserInputSchema().validate(data)
        if errors:
            return jsonify({"status": "Fail"})
        try:
            return jsonify({"status": Context.get_db_worker().insert_user(
                request.args["name"],
                generate_password_hash(request.args["password"]),
                request.args["role"]
            )})
        except Exception as error:
            logging.exception(error)
            return jsonify({"status": "Fail"})
