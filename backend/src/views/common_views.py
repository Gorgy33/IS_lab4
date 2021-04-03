from flask import render_template, make_response
from flask.views import MethodView
from flask_login import current_user, login_required

from backend.src.auth import roles_restriction


class Base(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN", "USER"])
    def get(self):
        return make_response(render_template("base.html", role=current_user.get_role()))
