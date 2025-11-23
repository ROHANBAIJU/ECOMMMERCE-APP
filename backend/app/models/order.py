from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.order import OrderStatus, ShippingAddress, OrderItemBase

class Order(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    items: List[OrderItemBase]
    total: float
    status: OrderStatus = OrderStatus.PENDING
    shipping_address: ShippingAddress
    payment_method: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        use_enum_values = True
