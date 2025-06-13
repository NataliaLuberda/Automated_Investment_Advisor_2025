from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, validates

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
    
    source = relationship("Account", foreign_keys=[source_account_id])
    target = relationship("Account", foreign_keys=[target_account_id])
    
    __table_args__ = (
        CheckConstraint('amount_numeric > 0', name='check_amount_positive'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.MAX_DESC_LENGTH = 128

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError("Description cannot be empty")
        if len(description) > self.MAX_DESC_LENGTH:
            raise ValueError(f"Description cannot be longer than {self.MAX_DESC_LENGTH} characters")
        return description

    @validates('amount_numeric')
    def validate_amount(self, key, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return amount

    @validates('source_account_id', 'target_account_id')
    def validate_accounts(self, key, account_id):
        if key == 'source_account_id' and account_id == self.target_account_id:
            raise ValueError("Source and target accounts cannot be the same")
        return account_id


class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(3), unique=True, nullable=False)
