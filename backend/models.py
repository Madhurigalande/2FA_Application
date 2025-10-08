import database
from sqlalchemy import Column, Integer, String, Boolean
Base = database.Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_2fa_enabled = Column(Boolean, default=False)
    otp_secret = Column(String(32), nullable=True)
