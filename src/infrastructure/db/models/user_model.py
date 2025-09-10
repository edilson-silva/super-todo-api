from sqlalchemy import Column, DateTime, String, Uuid

from ..session import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Uuid, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True))
