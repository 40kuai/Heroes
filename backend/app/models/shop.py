from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum


class ProductType(str, enum.Enum):
    ITEM = "item"
    CURRENCY = "currency"
    SPECIAL = "special"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(SQLEnum(ProductType), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="gold")  # gold, diamond
    quantity = Column(Integer, default=1)
    level_requirement = Column(Integer, default=1)
    is_active = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    currency = Column(String, default="gold")
    payment_status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
