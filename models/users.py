# from datetime import datetime, timezone
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean
from db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    fullname = Column(String, nullable=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    is_bot = Column(Boolean)
    language_code = Column(String)
