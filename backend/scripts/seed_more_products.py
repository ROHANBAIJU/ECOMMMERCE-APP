"""
Add more sample products to the database
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "ecommerce_db"

async def seed_more_products():
    """Add additional products to the database"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    print("🌱 Seeding additional products...")
    
    additional_products = [
        # More Electronics
        {
            "name": "Apple Watch Series 9",
            "description": "Advanced health and fitness tracking with always-on Retina display",
            "price": 429.99,
            "category": "Electronics",
            "stock": 75,
            "images": ["https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Samsung 55\" QLED 4K TV",
            "description": "Quantum dot technology with 4K resolution and HDR support",
            "price": 899.99,
            "category": "Electronics",
            "stock": 20,
            "images": ["https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Canon EOS R6 Camera",
            "description": "Full-frame mirrorless camera with 20MP sensor and 4K video",
            "price": 2499.99,
            "category": "Electronics",
            "stock": 15,
            "images": ["https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "PlayStation 5",
            "description": "Next-gen gaming console with 4K graphics and ultra-fast SSD",
            "price": 499.99,
            "category": "Electronics",
            "stock": 30,
            "images": ["https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # More Clothing
        {
            "name": "North Face Puffer Jacket",
            "description": "Warm insulated jacket perfect for cold weather",
            "price": 249.99,
            "category": "Clothing",
            "stock": 60,
            "images": ["https://images.unsplash.com/photo-1548126032-079b12adbf68?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Columbia Fleece Jacket",
            "description": "Comfortable fleece jacket for outdoor activities",
            "price": 79.99,
            "category": "Clothing",
            "stock": 90,
            "images": ["https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Under Armour T-Shirt",
            "description": "Moisture-wicking athletic t-shirt",
            "price": 29.99,
            "category": "Clothing",
            "stock": 150,
            "images": ["https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Timberland Boots",
            "description": "Durable waterproof leather boots",
            "price": 189.99,
            "category": "Clothing",
            "stock": 50,
            "images": ["https://images.unsplash.com/photo-1605812860427-4024433a70fd?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # More Books
        {
            "name": "Design Patterns",
            "description": "Elements of Reusable Object-Oriented Software",
            "price": 54.99,
            "category": "Books",
            "stock": 100,
            "images": ["https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Thinking, Fast and Slow",
            "description": "Daniel Kahneman's masterpiece on decision making",
            "price": 32.99,
            "category": "Books",
            "stock": 120,
            "images": ["https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # More Home & Kitchen
        {
            "name": "KitchenAid Stand Mixer",
            "description": "Professional 5-quart stand mixer for baking",
            "price": 449.99,
            "category": "Home",
            "stock": 35,
            "images": ["https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Philips Air Fryer",
            "description": "Healthy cooking with rapid air technology",
            "price": 129.99,
            "category": "Home",
            "stock": 65,
            "images": ["https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # More Sports
        {
            "name": "Fitbit Charge 6",
            "description": "Advanced fitness tracker with heart rate monitoring",
            "price": 179.99,
            "category": "Sports",
            "stock": 85,
            "images": ["https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Resistance Bands Set",
            "description": "5-piece resistance band set for strength training",
            "price": 24.99,
            "category": "Sports",
            "stock": 200,
            "images": ["https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.products.insert_many(additional_products)
    print(f"✅ Added {len(result.inserted_ids)} more products")
    print(f"   Total products in database: {await db.products.count_documents({})}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_more_products())
