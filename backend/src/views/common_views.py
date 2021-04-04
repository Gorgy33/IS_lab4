from flask import render_template, make_response, request, url_for, redirect, flash
from flask.views import MethodView
from flask_login import current_user, login_required

from backend.src.auth import roles_restriction
from backend.src.data.context import Context
from backend.src.views.schemas import AddNoteInputSchema, DeleteNoteInputScheme


class Base(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN", "USER"])
    def get(self):
        return make_response(render_template("base.html", role=current_user.get_role()))


class GetNoteList(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN", "USER"])
    def get(self):
        notes = Context.get_db_worker().get_notes()
        return make_response(render_template("notes.html", items=notes, role=current_user.get_role()))


class AddNote(MethodView):

    @login_required
    @roles_restriction(roles=["ADMIN", "USER"])
    def get(self):
        return make_response(render_template("add_note.html", role=current_user.get_role()))

    @login_required
    @roles_restriction(roles=["ADMIN", "USER"])
    def post(self):
        data = {'text': request.form['data']}
        errors = AddNoteInputSchema().validate(data)
        if errors:
            flash(errors, category='error')
            return redirect(url_for('note_list'))
        user = Context.get_db_worker().get_user(current_user.get_id())
        Context.get_db_worker().insert_notes(text=data['text'], author=user.nickname)
        return redirect(url_for('note_list'))


class DeleteNote(MethodView):
    @login_required
    @roles_restriction(roles=["ADMIN"])
    def get(self):
        data = request.args
        errors = DeleteNoteInputScheme().validate(data)
        if errors:
            flash(errors, 'error')
            return redirect(url_for('note_list'))
        try:
            Context.get_db_worker().delete_note(data['id'])
        except Exception as error:
            flash(error, 'error')
        return redirect(url_for('note_list'))
