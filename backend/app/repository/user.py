import logging
import pygogo as gogo
from typing import Dict
from sqlalchemy import func

from app.model.user import UserModel

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class UserRepository:

    def get(self, uuid: str, session=None) -> UserModel:
        logger.info(f"Get UserRepository for uuid: {uuid}")
        user = session.query(UserModel).get(uuid)
        return user

    def get_by_email(self, email, session=None):
        logger.info(f"get_by_email UserRepository for email: {email}")
        # El email del token service viene como una tupla
        user = session.query(UserModel).filter(UserModel.email == email[0]).first()
        return user

    def get_all_active(self, session=None, page: int = 1, per_page: int = 10):
        logger.info("get_all_active UserRepository")
        total = session.query(func.count(UserModel.id)).filter(UserModel.active).scalar()
        users = (
            session.query(UserModel)
            .filter(UserModel.active)
            .order_by(UserModel.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        return users, total

    def save(self, data: Dict, session=None) -> UserModel:
        try:
            user = UserModel()
            user.name = data['name']
            user.lastname = data.get('lastname')
            user.password = UserModel.get_hashed_password(data['password'])
            user.cellphone = data.get('cellphone')
            user.email = data['email']
            user.role_id = data['role_id']
            user.active = True
            session.add(user)
            session.commit()
            return user
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc
