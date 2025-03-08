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
    is_verified = Column(Boolean, nullable=False, default=False)
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
    balance = Column(Numeric(12, 2), nullable=False, default=0)
    bonus_balance = Column(Numeric(12, 2), nullable=False, default=0)
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
    source_type = Column(String, nullable=False)  # card/wallet
    source_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    dest_type = Column(String, nullable=False)  # card/wallet
    dest_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    
class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    merchant_name = Column(String, nullable=False)
    balance = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


class Categorie(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    deleted_at = Column(DateTime, nullable=True)


def migrate_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Миграции прошли успешно ✅")

    except Exception as e:
        print(f"Ошибка во время миграции: {e}")
