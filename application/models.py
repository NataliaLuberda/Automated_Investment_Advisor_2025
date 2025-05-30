from sqlalchemy import Column, Integer, String, Float, ForeignKey
from application.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
class Transakcja(Base):
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount_numeric = Column(Float(8), nullable=False)
    id_sender = Column(Integer, nullable=False)
    id_receiver = Column(Integer, nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    currency = relationship("Currency")
    
class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)