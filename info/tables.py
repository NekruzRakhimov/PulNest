import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime



class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(Integer, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    deleted_at = Column(DateTime, default=datetime.datetime.now())


class Wallets(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    phone = Column(Integer, unique=True, nullable=False)
    balance = Column(float, default=00.00)
    created_at = Column(DateTime, default=datetime.datetime.now())
    deleted_at = Column(DateTime, default=datetime.datetime.now())


class Cards(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_number = Column(Integer, unique=True, nullable=False)
    card_holder_name = Column(String, nullable=False)
    exp_date = Column()
    balance = Column(float, default=00.00)
    created_at = Column(DateTime, default=datetime.datetime.now())
    deleted_at = Column(DateTime, default=datetime.datetime.now())


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_type = Column(String, nullable=False)   #card/wallet
    source_id = Column(Integer, nullable=False)
    amount = Column(float, nullable=False)
    dest_type = Column(String, nullable=False)  #card/wallet
    dest_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    status = Column(String, nullable=False)
   

class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    subcategory = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    deleted_at = Column(DateTime, default=datetime.datetime.now())
   