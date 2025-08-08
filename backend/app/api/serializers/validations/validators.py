from marshmallow import ValidationError


def validate_password(n):
    if len(n) < 8:
        raise ValidationError('Password must be greater than 7 characters')
    if len(n) > 50:
        raise ValidationError('Password must not be greater than 50 characters')