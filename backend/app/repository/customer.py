import sqlalchemy
import logging
import pygogo as gogo
from typing import Dict
from sqlalchemy import func
from app.model.customer import CustomerModel

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class CustomerRepository:

    def get(self, uuid: str, session=None) -> CustomerModel:
        logger.info("Get CustomerRepository")
        customer = session.query(CustomerModel).get(uuid)
        return customer


    def get_all_active(self, session=None, page: int = 1, per_page: int = 10):
        logger.info("get_all_active CustomerRepository")
        total = session.query(func.count(CustomerModel.id)).filter(CustomerModel.active).scalar()
        customers = (
            session.query(CustomerModel)
            .filter(CustomerModel.active)
            .order_by(CustomerModel.order)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        return customers, total

    def save(self, data: Dict, user_id: str, session=None) -> CustomerModel:
        try:
            last_order = session.query(func.max(CustomerModel.order)).scalar()
            next_order = (last_order or 0) + 1

            customer = CustomerModel()
            customer.order = next_order
            customer.company_name = data['company_name']
            customer.person_type = data['person_type']
            customer.rfc = data['rfc']
            customer.legal_representative = data['legal_representative']
            customer.email = data['email']
            customer.phone = data['phone']
            customer.document = data['document']
            customer.active = True
            customer.created_by = user_id
            customer.updated_by = user_id
            session.add(customer)
            session.commit()
            return customer
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("Error de integridad, es posible que un cliente con datos similares ya exista.")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc

    def update(self, uuid: str, data: Dict, user_id: str, session=None) -> CustomerModel:
        try:
            customer = session.query(CustomerModel).get(uuid)
            if not customer or not customer.active:
                raise Exception("Cliente no encontrado.")

            for key, value in data.items():
                setattr(customer, key, value)

            customer.updated_by = user_id
            customer.updated_at = func.now()

            session.commit()
            return customer
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("Error de integridad, es posible que un cliente con datos similares ya exista.")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc

    def delete(self, uuid: str, user_id: str, session=None) -> CustomerModel:
        try:
            customer = session.query(CustomerModel).get(uuid)
            if not customer or not customer.active:
                raise Exception("Cliente no encontrado.")

            customer.active = False
            customer.updated_by = user_id
            customer.updated_at = func.now()
            session.commit()
            return customer
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc