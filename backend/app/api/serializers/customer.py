from marshmallow import Schema, fields, validate, pre_load
from app.utils.person_types import PersonType


class CustomerSchema(Schema):
    id = fields.Str()
    order = fields.Integer()
    company_name = fields.Str(required=True)
    person_type = fields.Str(
        required=True,
        validate=validate.OneOf(
            choices=[pt.value for pt in PersonType],
            error="El tipo de persona no es válido. Use '1' para persona física o '2' para moral."
        ))
    rfc = fields.Str(
        required=True,
        validate=validate.Regexp(
            regex=r'^[A-ZÑ&]{3,4}\d{6}[A-Z\d]{3}$',
            error='El formato del RFC no es válido. Debe contener 12 o 13 caracteres.'
        ))
    legal_representative = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True, validate=validate.Regexp(
            regex=r'^\d{10}$',
            error='Formato de teléfono inválido, debe contener 10 dígitos. Ejemplo: 9992193445'
        ))
    document = fields.Str(required=True)

    @pre_load
    def uppercase_rfc(self, data, **kwargs):
        if data.get('rfc') and isinstance(data.get('rfc'), str):
            data['rfc'] = data['rfc'].upper().strip()
        return data
