from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str
    price: float = Field(..., gt=0)
    category: str
    stock: int = Field(..., ge=0)
    images: List[str] = []
    specifications: dict = {}

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)
    images: Optional[List[str]] = None
    specifications: Optional[dict] = None

class ProductResponse(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProductList(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    pages: int
