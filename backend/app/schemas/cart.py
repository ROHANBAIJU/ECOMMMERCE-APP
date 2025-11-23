from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class CartItemBase(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)

class CartItemAdd(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)

class CartItem(CartItemBase):
    id: str
    product_name: str
    product_price: float
    product_image: str
    subtotal: float
    
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    user_id: str
    items: List[CartItem]
    total: float
    item_count: int
    updated_at: datetime
    
    class Config:
        from_attributes = True
