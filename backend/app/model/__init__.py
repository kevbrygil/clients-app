"""
    author: Gilbert Tamayo
    date: 23/10/2019
    email: <tamayo_144@hotmail.com>
"""

# Se importan los modelos para que sqlalchemy pueda generar las tablas, si estas no existen
from .user import UserModel
from .role import RoleModel
from .token import TokenModel
from .customer import CustomerModel

from app.database.sqlalchemy.connection import engine, Base, Session

Session = Session


def db_init():
    """ Initialize database """
    # Recreate database each time for demo
    # #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
