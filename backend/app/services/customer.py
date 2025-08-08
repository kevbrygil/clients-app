from app.repository.customer import CustomerRepository
from app.api.serializers.customer import CustomerSchema
from marshmallow import ValidationError
from app.api.exceptions.exceptions import SerializerException
import math


class CustomerService:
    def __init__(self):
        self.customer_repo = CustomerRepository()
        self.customer_schema = CustomerSchema()

    def get_all(self, session, page: int, per_page: int):
        """devuelve los clientes de forma paginada."""
        try:
            customers, total = self.customer_repo.get_all_active(session, page, per_page)
            _customers = CustomerSchema(many=True).dump(customers)
            return {
                "items": _customers,
                "page": page,
                "per_page": per_page,
                "total_pages": math.ceil(total / per_page) if total > 0 else 0,
                "total_items": total,
            }
        except Exception as exc:
            print("Service get_all error {}".format(exc))
            raise exc

    def get_by_id(self, uuid, session):
        """Obtiene un cliente mediante su id"""
        try:
            customer = self.customer_repo.get(uuid, session)
            _customer = self.customer_schema.dump(customer)
            return _customer
        except Exception as exc:
            print("Service get_by_id error {}".format(exc))
            raise exc
        
    def create(self, data, user, session):
        """crea un cliente en el sistema"""
        try:
            if isinstance(data, dict) and data:
                _customer = {}
                try:
                    # valida los datos
                    _customer = CustomerSchema().load(data)
                    print(_customer)
                except ValidationError as err:
                    raise err
                customer = self.customer_repo.save(_customer, user['user_id'], session)
                result = self.customer_schema.dump(customer)
                return result
        except ValidationError as err:
            raise err
        except SerializerException as exc:
            print(f"Service create error serializer {exc}")
            raise exc
        except Exception as exc:
            print(f"Service create error {exc}")
            raise exc

    def update(self, uuid, data, user, session):
        """actualiza un cliente en el sistema"""
        try:
            if not isinstance(data, dict) or not data:
                raise Exception("Datos inválidos.")

            try:
                # partial=True permite actualizaciones parciales
                validated_data = CustomerSchema(partial=True).load(data)
            except ValidationError as err:
                raise err

            customer = self.customer_repo.update(uuid, validated_data, user['user_id'], session)
            result = self.customer_schema.dump(customer)
            return result
        except ValidationError as err:
            raise err
        except Exception as exc:
            print(f"Service update error {exc}")
            raise exc

    def delete(self, uuid, user, session):
        """Elimina (desactiva) un cliente del sistema"""
        try:
            customer = self.customer_repo.delete(uuid, user['user_id'], session)
            return {"id": customer.id, "status": "deleted"}
        except Exception as exc:
            print(f"Service delete error {exc}")
            raise exc
