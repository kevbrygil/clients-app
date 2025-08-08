import logging
import pygogo as gogo
import math

from app.api.exceptions.exceptions import SerializerException
from app.repository.user import UserRepository
from app.api.serializers.user import UserSchema
from marshmallow import ValidationError

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class UserService:
    def __init__(self):
        self.user_rep = UserRepository()
        self.user_schema = UserSchema()

    def get_all(self, session, page: int, per_page: int):
        """devuelve los usuarios que se encuentran en el sistema de forma paginada."""
        try:
            users, total = self.user_rep.get_all_active(session, page, per_page)
            _users = UserSchema(many=True).dump(users)
            return {
                "items": _users,
                "page": page,
                "per_page": per_page,
                "total_pages": math.ceil(total / per_page) if total > 0 else 0,
                "total_items": total,
            }
        except Exception as exc:
            logger.error(f"Service get_all error {exc}")
            raise exc

    def create(self, data, session):
        """crea un usuario y devuelve un diccionario con los datos del usuario y rol"""
        try:
            print("En service user")
            if isinstance(data, dict) and data:
                _user = {}
                try:
                    _user = UserSchema().load(data)
                except ValidationError as err:
                    raise err
                user = self.user_rep.save(_user, session)
                result = self.user_schema.dump(user)
                print(result)
                print(type(result))
                return result
        except ValidationError as err:
            logger.error("ValidationError")
            logger.error(err)
            raise err
        except SerializerException as err:
            logger.error("SerializerException")
            logger.error(err)
            raise err
        except Exception as err:
            logger.error("Exception")
            logger.error(err)
            raise err
