import re
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length
from backend.src.data.context import Context


def new_password_check(password: str):
    if len(password) < 8:
        raise ValidationError('Password length should be 8 or more')
    if not re.search(r'\d', password):
        raise ValidationError('Password must be contain numbers')
    if not re.search(r'\W', password):
        raise ValidationError('Password must be contain special symbols')


def role_check(role: str):
    if role.upper() not in ('ADMIN', 'USER'):
        raise ValidationError('Invalid role')


def login_check(login: str):
    if re.search(r'\s', login):
        raise ValidationError('Login should not contain spaces')


def new_login_check(login: str):
    users = Context.get_db_worker().get_users()
    users = [user.login for user in users]
    if not 6 < len(login) < 20:
        raise ValidationError('Login length should be 6 or more symbols bt less then 20')
    if login in users:
        raise ValidationError('Login should be unique')


class CreateUserInputSchema(Schema):
    name = fields.String(required=True, validate=new_login_check)
    password = fields.String(required=True, validate=new_password_check)
    role = fields.String(required=True, validate=role_check)
    nickname = fields.String(required=True, validate=Length(min=1))


class LoginInputSchema(Schema):
    name = fields.String(required=True, validate=login_check)
    password = fields.String(required=True)


class AddNoteInputSchema(Schema):
    text = fields.String(required=True, validate=Length(min=1, max=100))


class DeleteNoteInputScheme(Schema):
    id = fields.String(required=True)
