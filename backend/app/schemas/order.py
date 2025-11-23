from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class ShippingAddress(BaseModel):
    full_name: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    phone: str

class OrderItemBase(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(..., gt=0)
    price: float
    subtotal: float

class OrderItem(OrderItemBase):
    id: str
    
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    shipping_address: ShippingAddress
    payment_method: str

class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    total: float
    status: OrderStatus
    shipping_address: ShippingAddress
    payment_method: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class OrderList(BaseModel):
    orders: List[OrderResponse]
    total: int
    page: int
    pages: int
