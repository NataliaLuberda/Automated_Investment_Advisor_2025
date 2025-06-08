from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from application.services.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(10), nullable=False)
    balance = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="accounts")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    default_currency = Column(String(10), nullable=True)
    accounts = relationship("Account", back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount_numeric = Column(Float(8), nullable=False)
    target_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    source_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.now())
    description = Column(String(128), nullable=False)
    source = relationship("Account", foreign_keys=[target_account_id])
    target = relationship("Account", foreign_keys=[source_account_id])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.MAX_DESC_LENGTH = 128


class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(3), unique=True, nullable=False)
