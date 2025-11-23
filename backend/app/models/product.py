from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    description: str
    price: float
    category: str
    stock: int
    images: List[str] = []
    specifications: dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": 999.99,
                "category": "Electronics",
                "stock": 50,
                "images": ["image1.jpg", "image2.jpg"],
                "specifications": {
                    "brand": "TechBrand",
                    "model": "X200",
                    "ram": "16GB",
                    "storage": "512GB SSD"
                }
            }
        }
