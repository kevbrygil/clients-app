import falcon
from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.services.user import UserService
from app.utils.api_response import response_ok, response_error
from app.api.hooks.auth import validate_token
from app.api.hooks.validate_role import validate_scope_admin


@falcon.before(validate_token)
class User:
    def __init__(self):
        self.user_service = UserService()

    @falcon.before(validate_scope_admin)
    def on_get(self, req, resp):
        """Obtiene los usuarios de forma paginada."""
        try:
            page = int(req.params.get('page', 1))
            per_page = int(req.params.get('per_page', 10))
            if page < 1 or per_page < 1:
                raise ValueError("Los parámetros de paginación deben ser números positivos.")

            result = self.user_service.get_all(self.session, page, per_page)
            resp.status = falcon.HTTP_200
            resp.context['result'] = response_ok(result, "ok", 'list of users', 'get', req.path)
        except ValueError as e:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error({}, f"Parámetros inválidos: {e}", 'get', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'get', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Internal Error. Contact the Admin.", 'get', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error({}, str(exc), 'get', req.path)

    @falcon.before(validate_scope_admin)
    def on_post(self, req, resp):
        """crea un usuario para el sistema con su rol"""
        try:
            result = self.user_service.create(req.context['data'], self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'created', 'post', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'post', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Internal Error. Contact the Admin.", 'post', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error({}, str(exc), 'post', req.path)
