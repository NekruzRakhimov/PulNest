from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
import datetime
from db.postgres import engine


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    phone = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.00)
    created_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_number = Column(String, unique=True, nullable=False)
    card_holder_name = Column(String, nullable=False)
    exp_date = Column(String, nullable=False)
    cvv = Column(String, nullable=False)
    balance = Column(Float, default=0.00) 
    created_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_type = Column(String, nullable=False)  # card/wallet
    source_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    dest_type = Column(String, nullable=False)  # card/wallet
    dest_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    status = Column(String, nullable=False)


class Services(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=False)
    merchant_name = Column(String, nullable=False)
    balance = Column(Float, default=0.00)
    created_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


def migrate_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Миграции прошли успешно ✅")
    except Exception as e:
        print(f"Ошибка во время миграции: {e}")
