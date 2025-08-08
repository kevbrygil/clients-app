import falcon
from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.api.hooks.auth import validate_token
from app.services.customer import CustomerService
from app.utils.api_response import response_ok, response_error
from app.api.hooks.validate_role import validate_scope_admin, validate_scope_both

@falcon.before(validate_token)
class Customer:
    def __init__(self):
        self.customer_service = CustomerService()

    @falcon.before(validate_scope_both)
    def on_get(self, req, resp):
        """Obtiene los clientes de forma paginada y ordenada por el campo 'order'."""
        try:
            page = int(req.params.get('page', 1))
            per_page = int(req.params.get('per_page', 10))
            if page < 1 or per_page < 1:
                raise ValueError("Los parámetros de paginación deben ser números positivos.")

            result = self.customer_service.get_all(self.session, page, per_page)
            resp.status = falcon.HTTP_200
            resp.context['result'] = response_ok(result, "ok", 'list of customers', 'get', req.path)
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
        """Crea un cliente"""
        try:
            result = self.customer_service.create(req.context['data'], req.context['user'], self.session)
            resp.status = falcon.HTTP_201
            resp.context['result'] = response_ok(result, "ok", 'created', 'post', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'post', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error(str(exc), "Internal Error. Contact the Admin.", 'post', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(str(exc), "Error", 'post', req.path)


@falcon.before(validate_token)
class CustomerResource:
    def __init__(self):
        self.customer_service = CustomerService()

    @falcon.before(validate_scope_both)
    def on_get(self, req, resp, uuid):
        """Obtiene un cliente por su id"""
        try:
            result = self.customer_service.get_by_id(uuid, self.session)
            if not result:
                resp.status = falcon.HTTP_404
                resp.context['result'] = response_error({}, "Cliente no encontrado.", 'get', req.path)
                return
            resp.status = falcon.HTTP_200
            resp.context['result'] = response_ok(result, "ok", 'customer by id', 'get', req.path)
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
    def on_put(self, req, resp, uuid):
        """Actualiza un cliente por su id"""
        try:
            result = self.customer_service.update(uuid, req.context['data'], req.context['user'], self.session)
            resp.status = falcon.HTTP_200
            resp.context['result'] = response_ok(result, "ok", 'customer updated', 'put', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, "Validation Error", 'put', req.path)
        except Exception as exc:
            if "Cliente no encontrado" in str(exc):
                resp.status = falcon.HTTP_404
                resp.context['result'] = response_error({}, str(exc), 'put', req.path)
            else:
                resp.status = falcon.HTTP_400
                resp.context['result'] = response_error({}, str(exc), 'put', req.path)

    @falcon.before(validate_scope_admin)
    def on_delete(self, req, resp, uuid):
        """Elimina (desactiva) un cliente por su id"""
        try:
            self.customer_service.delete(uuid, req.context['user'], self.session)
            resp.status = falcon.HTTP_200
            resp.context['result'] = response_ok({}, "ok", 'customer deleted', 'delete', req.path)
        except Exception as exc:
            if "Cliente no encontrado" in str(exc):
                resp.status = falcon.HTTP_404
                resp.context['result'] = response_error({}, str(exc), 'delete', req.path)
            else:
                resp.status = falcon.HTTP_400
                resp.context['result'] = response_error({}, str(exc), 'delete', req.path)
