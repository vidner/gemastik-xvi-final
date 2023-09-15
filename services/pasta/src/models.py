from database import Base
from sqlalchemy import Column, String, Boolean


class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=True)
