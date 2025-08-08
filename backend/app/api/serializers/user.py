from marshmallow import Schema, fields, validate
from .role import RoleSchema
from .validations.validators import validate_password


class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    lastname = fields.Str()
    password = fields.Str(required=True, load_only=True, validate=validate_password)
    cellphone = fields.Str(validate=validate.Regexp(
            regex = r'^(\d{10})$', flags = 0,
            error = 'Formato de teléfono inválido, debe contener 10 dígitos. Ejemplo: 9992193445'
        ))
    email = fields.Email(required=True)
    status = fields.Str()
    role_id = fields.Str(required=True, load_only=True)
    role = fields.Nested(RoleSchema, load_only=False)
    created_at = fields.DateTime()
    updated_at = fields.Str()
