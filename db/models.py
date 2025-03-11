import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Numeric, Boolean

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
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


class VerificationCode(Base):
    __tablename__ = "verification_codes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    email = Column(String(255), nullable=False)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    phone = Column(String, unique=True, nullable=False)
    balance = Column(Numeric(12, 2), default=0)
    bonus_balance = Column(Numeric(12, 2),default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_number = Column(String, unique=True, nullable=False)
    card_holder_name = Column(String, nullable=False)
    exp_date = Column(String, nullable=False)
    cvv = Column(String, nullable=False)
    balance = Column(Numeric(precision=12, scale=2), default=0)
    created_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tran_type = Column(String, nullable=False) # income, expense
    source_type = Column(String, nullable=False)  
    source_id = Column(Integer, nullable=False)
    source_number = Column(String, nullable=False) #добавила
    amount = Column(Float, nullable=False)
    dest_type = Column(String, nullable=False)  
    dest_id = Column(Integer, nullable=False)
    dest_number = Column(String, nullable=False) #добавила
    comment = Column(String) 
    correlation_id = Column(Integer)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    
class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    provider_name = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


def migrate_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Миграции прошли успешно ✅")

    except Exception as e:
        print(f"Ошибка во время миграции: {e}")
