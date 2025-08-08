"""Script que iniciliza la bd con sus tablas y los roles necesarios"""

import logging
from app.model import db_init, Session
from app.model.role import RoleModel
from app.model.user import UserModel
import pygogo as gogo


log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo('BD-SCRIPT', low_formatter=formatter).logger

session = Session()
logger.info("Creando BD y tablas...")
try:
    db_init()
except Exception as err:
    logger.error("No se ha podido crear la bd")
    logger.error(err)
    raise err

logger.info("Creando roles y usuarios admin y viewer")
exist = session.query(RoleModel).filter(RoleModel.name == "admin").first()
if exist is None:
    adminRole = RoleModel()
    adminRole.name = 'admin'
    adminRole.active = True
    session.add(adminRole)
    session.commit()
    existUser = session.query(UserModel).filter(UserModel.email == "admin@challenge.com").first()
    if existUser is None:
        adminUser = UserModel()
        adminUser.email = "admin@challenge.com"
        adminUser.name = "admin"
        adminUser.lastname = "admin"
        adminUser.password = UserModel.get_hashed_password("123456789")
        adminUser.cellphone = "123456789"
        adminUser.status = "active"
        adminUser.active = True
        adminUser.role_id = adminRole.id
        session.add(adminUser)
        session.commit()


exist = session.query(RoleModel).filter(RoleModel.name == "viewer").first()
if exist is None:
    viewerRole = RoleModel()
    viewerRole.name = 'viewer'
    viewerRole.active = True
    session.add(viewerRole)
    session.commit()
    existUser = session.query(UserModel).filter(UserModel.email == "viewer@challenge.com").first()
    if existUser is None:
        viewerUser = UserModel()
        viewerUser.email = "viewer@challenge.com"
        viewerUser.name = "viewer"
        viewerUser.lastname = "viewer"
        viewerUser.password = UserModel.get_hashed_password("123456789")
        viewerUser.cellphone = "123456789"
        viewerUser.status = "active"
        viewerUser.active = True
        viewerUser.role_id = viewerRole.id
        session.add(viewerUser)
        session.commit()
