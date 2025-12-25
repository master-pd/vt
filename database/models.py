# -*- coding: utf-8 -*-
"""
DATABASE MODELS - SQLALCHEMY MODELS
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import Config

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    join_date = Column(DateTime, default=datetime.now)
    total_tests = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime)
    language = Column(String(10), default='en')
    
    # Relationships
    tests = relationship("Test", back_populates="user")
    orders = relationship("Order", back_populates="user")

class Test(Base):
    __tablename__ = 'tests'
    
    id = Column(Integer, primary_key=True)
    test_id = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    video_url = Column(Text, nullable=False)
    target_views = Column(Integer, nullable=False)
    views_sent = Column(Integer, default=0)
    views_verified = Column(Integer, default=0)
    success_rate = Column(Float, default=0)
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime)
    status = Column(String(20), default='pending')  # pending, running, completed, failed
    duration = Column(Float)  # in seconds
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="tests")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    test_id = Column(String(50), ForeignKey('tests.test_id'))
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default='USD')
    status = Column(String(20), default='pending')  # pending, paid, completed, refunded
    payment_method = Column(String(50))
    payment_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    test = relationship("Test")

class TikTokAccount(Base):
    __tablename__ = 'tiktok_accounts'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))
    status = Column(String(20), default='active')  # active, banned, limited, disabled
    views_sent = Column(Integer, default=0)
    last_used = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    notes = Column(Text)

class Proxy(Base):
    __tablename__ = 'proxies'
    
    id = Column(Integer, primary_key=True)
    proxy = Column(String(500), unique=True, nullable=False)
    proxy_type = Column(String(20), default='http')  # http, https, socks4, socks5
    country = Column(String(50))
    city = Column(String(100))
    speed = Column(Integer)  # in milliseconds
    last_used = Column(DateTime)
    last_checked = Column(DateTime)
    success_rate = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

class SystemLog(Base):
    __tablename__ = 'system_logs'
    
    id = Column(Integer, primary_key=True)
    level = Column(String(20))  # INFO, WARNING, ERROR, DEBUG
    module = Column(String(100))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, nullable=True)
    ip_address = Column(String(50))
    user_agent = Column(String(500))

class Configuration(Base):
    __tablename__ = 'configurations'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    data_type = Column(String(20))  # string, integer, float, boolean, json
    category = Column(String(50))
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Database engine and session
engine = create_engine(f'sqlite:///{Config.DATABASE_PATH}')
Session = sessionmaker(bind=engine)

def init_database():
    """Initialize database tables"""
    Base.metadata.create_all(engine)
    
def get_session():
    """Get database session"""
    return Session()