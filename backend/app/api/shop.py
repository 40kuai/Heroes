from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.shop import Product, Order, PaymentStatus
from app.models.user import User
from app.schemas.shop import ProductCreate, ProductResponse, OrderCreate, OrderResponse, RechargeRequest, RechargeResponse
from typing import List

router = APIRouter()


@router.post("/products", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """创建商品"""
    # 创建商品
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "type": product.type,
        "price": product.price,
        "currency": product.currency,
        "quantity": product.quantity,
        "level_requirement": product.level_requirement,
        "is_active": product.is_active,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }


@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """获取商品列表"""
    products = db.query(Product).filter(Product.is_active == PaymentStatus.PENDING).all()
    
    return [{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "type": product.type,
        "price": product.price,
        "currency": product.currency,
        "quantity": product.quantity,
        "level_requirement": product.level_requirement,
        "is_active": product.is_active,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    } for product in products]


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取单个商品详情"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "type": product.type,
        "price": product.price,
        "currency": product.currency,
        "quantity": product.quantity,
        "level_requirement": product.level_requirement,
        "is_active": product.is_active,
        "created_at": product.created_at,
        "updated_at": product.updated_at
    }


@router.post("/orders", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """创建订单"""
    # 检查用户是否存在
    user = db.query(User).filter(User.id == order_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查商品是否存在
    product = db.query(Product).filter(Product.id == order_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    # 检查商品是否激活
    if product.is_active != PaymentStatus.PENDING:
        raise HTTPException(status_code=400, detail="商品未激活")
    
    # 计算总价
    total_price = product.price * order_data.quantity
    
    # 创建订单
    order = Order(
        user_id=order_data.user_id,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        total_price=total_price,
        currency=product.currency,
        payment_status=PaymentStatus.PENDING
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return {
        "id": order.id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": order.total_price,
        "currency": order.currency,
        "payment_status": order.payment_status,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    }


@router.get("/orders/{user_id}", response_model=List[OrderResponse])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    """获取用户订单列表"""
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    
    return [{
        "id": order.id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": order.total_price,
        "currency": order.currency,
        "payment_status": order.payment_status,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    } for order in orders]


@router.post("/orders/{order_id}/pay", response_model=OrderResponse)
def pay_order(order_id: int, db: Session = Depends(get_db)):
    """支付订单"""
    # 查找订单
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 检查订单状态
    if order.payment_status != PaymentStatus.PENDING:
        raise HTTPException(status_code=400, detail="订单状态不正确")
    
    # 更新订单状态为已完成
    order.payment_status = PaymentStatus.COMPLETED
    db.commit()
    db.refresh(order)
    
    return {
        "id": order.id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": order.total_price,
        "currency": order.currency,
        "payment_status": order.payment_status,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    }


@router.post("/recharge", response_model=RechargeResponse)
def recharge(recharge_data: RechargeRequest, db: Session = Depends(get_db)):
    """充值"""
    # 检查用户是否存在
    user = db.query(User).filter(User.id == recharge_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 创建充值订单（这里简化处理，实际应该创建一个专门的充值记录）
    # 为了演示，我们创建一个特殊的订单来表示充值
    recharge_product = Product(
        name=f"充值{recharge_data.amount}{recharge_data.currency}",
        description="货币充值",
        type="currency",
        price=recharge_data.amount,
        currency=recharge_data.currency,
        quantity=1,
        level_requirement=1,
        is_active=PaymentStatus.PENDING
    )
    db.add(recharge_product)
    db.commit()
    db.refresh(recharge_product)
    
    # 创建订单
    order = Order(
        user_id=recharge_data.user_id,
        product_id=recharge_product.id,
        quantity=1,
        total_price=recharge_data.amount,
        currency=recharge_data.currency,
        payment_status=PaymentStatus.COMPLETED
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return {
        "id": order.id,
        "user_id": order.user_id,
        "amount": recharge_data.amount,
        "currency": recharge_data.currency,
        "payment_status": order.payment_status,
        "created_at": order.created_at
    }
