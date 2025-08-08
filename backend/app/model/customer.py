from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.sqlalchemy.connection import Base


class CustomerModel(Base):
    __tablename__ = 'customers'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    order = Column(Integer, autoincrement=True)
    company_name = Column(String)
    person_type = Column(String)
    rfc = Column(String, unique=True)
    legal_representative = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    document = Column(String)
    active = Column(Boolean, default=True)
    created_by = Column(UUID)
    updated_by = Column(UUID)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
