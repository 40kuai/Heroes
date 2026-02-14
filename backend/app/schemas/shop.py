from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.shop import ProductType, PaymentStatus


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: ProductType
    price: float
    currency: str = "gold"
    quantity: int = 1
    level_requirement: int = 1


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    is_active: PaymentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(OrderBase):
    user_id: int


class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_price: float
    currency: str
    payment_status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RechargeRequest(BaseModel):
    user_id: int
    amount: float
    currency: str = "diamond"


class RechargeResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    payment_status: PaymentStatus
    created_at: datetime

    class Config:
        from_attributes = True
