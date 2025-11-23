from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class CartItem(BaseModel):
    product_id: str
    quantity: int
    
class Cart(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    items: List[CartItem] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
