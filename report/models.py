from sqlalchemy import Column, Integer, String, Boolean, Float, Date, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)


class Tariff(Base):
    __tablename__ = "tariff"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    price_per_minute = Column(Float, nullable=False)


class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    tariff_id = Column(Integer, nullable=False)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(13), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    balance = Column(Float, nullable=True)


class Call(Base):
    __tablename__ = "call"

    id = Column(Integer, primary_key=True)
    caller_id = Column(Integer, nullable=False)
    called_id = Column(Integer, nullable=False)
    status_id = Column(Integer, nullable=False)
    document_id = Column(Integer, nullable=False)
    duration = Column(String(50), nullable=False)
    call_date = Column(DateTime, nullable=False)
