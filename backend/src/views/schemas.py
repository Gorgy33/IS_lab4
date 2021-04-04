from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Length
import re


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


class CreateUserInputSchema(Schema):
    name = fields.String(required=True, validate=Length(min=6, max=20))
    password = fields.String(required=True, validate=new_password_check)
    role = fields.String(required=True, validate=role_check)


class LoginInputSchema(Schema):
    name = fields.String(required=True, validate=login_check)
    password = fields.String(required=True)
