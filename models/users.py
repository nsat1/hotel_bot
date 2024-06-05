from sqlalchemy import Column, BigInteger, String, DateTime
from db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    fullname = Column(String, nullable=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    language_code = Column(String)
