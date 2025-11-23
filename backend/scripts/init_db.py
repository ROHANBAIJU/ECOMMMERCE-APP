"""
MongoDB Database Initialization Script
Creates collections, indexes, and populates with sample data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from app.core.security import get_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "ecommerce_db"

async def init_database():
    """Initialize database with collections, indexes, and sample data"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    print("🚀 Starting database initialization...")
    
    # Drop existing collections (optional - comment out if you want to preserve data)
    print("🗑️  Dropping existing collections...")
    await db.users.drop()
    await db.products.drop()
    await db.carts.drop()
    await db.orders.drop()
    
    # Create indexes
    print("📊 Creating indexes...")
    
    # Users indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("created_at")
    
    # Products indexes
    await db.products.create_index("category")
    await db.products.create_index("price")
    await db.products.create_index([("name", "text"), ("description", "text")])
    await db.products.create_index("created_at")
    
    # Carts indexes
    await db.carts.create_index("user_id", unique=True)
    
    # Orders indexes
    await db.orders.create_index("user_id")
    await db.orders.create_index("status")
    await db.orders.create_index("created_at")
    
    print("✅ Indexes created successfully!")
    
    # Insert sample users
    print("👥 Creating sample users...")
    users = [
        {
            "email": "admin@ecommerce.com",
            "hashed_password": get_password_hash("admin123"),
            "first_name": "Admin",
            "last_name": "User",
            "phone": "+1234567890",
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "email": "john@example.com",
            "hashed_password": get_password_hash("password123"),
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567891",
            "is_active": True,
            "is_admin": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "email": "jane@example.com",
            "hashed_password": get_password_hash("password123"),
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "+1234567892",
            "is_active": True,
            "is_admin": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.users.insert_many(users)
    print(f"✅ Created {len(result.inserted_ids)} users")
    admin_id = str(result.inserted_ids[0])
    user1_id = str(result.inserted_ids[1])
    user2_id = str(result.inserted_ids[2])
    
    # Insert sample products
    print("📦 Creating sample products...")
    products = [
        # Electronics
        {
            "name": "iPhone 15 Pro",
            "description": "Latest Apple iPhone with A17 Pro chip, titanium design, and advanced camera system",
            "price": 999.99,
            "category": "Electronics",
            "stock": 50,
            "images": [
                "https://images.unsplash.com/photo-1696446702183-cbd88e2adecb?w=500",
                "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Samsung Galaxy S24 Ultra",
            "description": "Flagship Samsung smartphone with S Pen, 200MP camera, and AI features",
            "price": 1199.99,
            "category": "Electronics",
            "stock": 35,
            "images": [
                "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "MacBook Pro 16\"",
            "description": "Apple MacBook Pro with M3 Max chip, 16GB RAM, 512GB SSD",
            "price": 2499.99,
            "category": "Electronics",
            "stock": 25,
            "images": [
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Sony WH-1000XM5",
            "description": "Premium wireless noise-canceling headphones with industry-leading sound quality",
            "price": 399.99,
            "category": "Electronics",
            "stock": 100,
            "images": [
                "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "iPad Air 11\"",
            "description": "Powerful iPad Air with M2 chip, perfect for creativity and productivity",
            "price": 599.99,
            "category": "Electronics",
            "stock": 60,
            "images": [
                "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # Clothing
        {
            "name": "Nike Air Max 270",
            "description": "Comfortable and stylish running shoes with Air Max cushioning",
            "price": 149.99,
            "category": "Clothing",
            "stock": 80,
            "images": [
                "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Levi's 501 Original Jeans",
            "description": "Classic straight-fit jeans, the original since 1873",
            "price": 89.99,
            "category": "Clothing",
            "stock": 120,
            "images": [
                "https://images.unsplash.com/photo-1542272454315-7f6d74f2c8b8?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Adidas Originals Hoodie",
            "description": "Comfortable cotton-blend hoodie with classic trefoil logo",
            "price": 79.99,
            "category": "Clothing",
            "stock": 95,
            "images": [
                "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Ray-Ban Aviator Sunglasses",
            "description": "Iconic aviator sunglasses with UV protection",
            "price": 159.99,
            "category": "Clothing",
            "stock": 70,
            "images": [
                "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # Books
        {
            "name": "The Pragmatic Programmer",
            "description": "Your journey to mastery - 20th Anniversary Edition",
            "price": 44.99,
            "category": "Books",
            "stock": 150,
            "images": [
                "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Clean Code",
            "description": "A Handbook of Agile Software Craftsmanship by Robert C. Martin",
            "price": 39.99,
            "category": "Books",
            "stock": 200,
            "images": [
                "https://images.unsplash.com/photo-1589998059171-988d887df646?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Atomic Habits",
            "description": "An Easy & Proven Way to Build Good Habits & Break Bad Ones",
            "price": 27.99,
            "category": "Books",
            "stock": 180,
            "images": [
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # Home & Kitchen
        {
            "name": "Instant Pot Duo 7-in-1",
            "description": "Electric pressure cooker, slow cooker, rice cooker, and more",
            "price": 89.99,
            "category": "Home",
            "stock": 45,
            "images": [
                "https://images.unsplash.com/photo-1585515320310-259814833e62?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Dyson V15 Detect",
            "description": "Cordless vacuum cleaner with laser dust detection",
            "price": 649.99,
            "category": "Home",
            "stock": 30,
            "images": [
                "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Nespresso Vertuo Next",
            "description": "Coffee and espresso maker with advanced extraction technology",
            "price": 179.99,
            "category": "Home",
            "stock": 55,
            "images": [
                "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # Sports & Outdoors
        {
            "name": "Yoga Mat Premium",
            "description": "Non-slip exercise mat with extra cushioning, 6mm thick",
            "price": 39.99,
            "category": "Sports",
            "stock": 200,
            "images": [
                "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Adjustable Dumbbells Set",
            "description": "Space-saving adjustable dumbbells, 5-52.5 lbs per dumbbell",
            "price": 299.99,
            "category": "Sports",
            "stock": 40,
            "images": [
                "https://images.unsplash.com/photo-1638536532686-d610adfc8e5c?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Hydro Flask Water Bottle",
            "description": "Insulated stainless steel water bottle, keeps cold 24 hours",
            "price": 44.95,
            "category": "Sports",
            "stock": 150,
            "images": [
                "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.products.insert_many(products)
    print(f"✅ Created {len(result.inserted_ids)} products")
    product_ids = [str(id) for id in result.inserted_ids]
    
    # Create empty carts for users
    print("🛒 Creating empty carts...")
    carts = [
        {
            "user_id": user1_id,
            "items": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "user_id": user2_id,
            "items": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    await db.carts.insert_many(carts)
    print(f"✅ Created {len(carts)} carts")
    
    # Create sample orders
    print("📝 Creating sample orders...")
    from app.schemas.order import OrderStatus
    
    orders = [
        {
            "user_id": user1_id,
            "items": [
                {
                    "product_id": product_ids[0],
                    "product_name": "iPhone 15 Pro",
                    "quantity": 1,
                    "price": 999.99,
                    "subtotal": 999.99
                },
                {
                    "product_id": product_ids[3],
                    "product_name": "Sony WH-1000XM5",
                    "quantity": 1,
                    "price": 399.99,
                    "subtotal": 399.99
                }
            ],
            "total": 1399.98,
            "status": OrderStatus.DELIVERED,
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            },
            "payment_method": "credit_card",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "user_id": user2_id,
            "items": [
                {
                    "product_id": product_ids[2],
                    "product_name": "MacBook Pro 16\"",
                    "quantity": 1,
                    "price": 2499.99,
                    "subtotal": 2499.99
                }
            ],
            "total": 2499.99,
            "status": OrderStatus.PROCESSING,
            "shipping_address": {
                "street": "456 Oak Ave",
                "city": "Los Angeles",
                "state": "CA",
                "zip_code": "90001",
                "country": "USA"
            },
            "payment_method": "paypal",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "user_id": user1_id,
            "items": [
                {
                    "product_id": product_ids[5],
                    "product_name": "Nike Air Max 270",
                    "quantity": 2,
                    "price": 149.99,
                    "subtotal": 299.98
                }
            ],
            "total": 299.98,
            "status": OrderStatus.SHIPPED,
            "shipping_address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "USA"
            },
            "payment_method": "credit_card",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.orders.insert_many(orders)
    print(f"✅ Created {len(result.inserted_ids)} orders")
    
    print("\n" + "="*60)
    print("✨ Database initialization completed successfully! ✨")
    print("="*60)
    print("\n📊 Summary:")
    print(f"   - Database: {DATABASE_NAME}")
    print(f"   - Users: {len(users)} (including 1 admin)")
    print(f"   - Products: {len(products)} across multiple categories")
    print(f"   - Carts: {len(carts)}")
    print(f"   - Orders: {len(orders)}")
    print("\n🔑 Test Credentials:")
    print("   Admin:")
    print("     Email: admin@ecommerce.com")
    print("     Password: admin123")
    print("\n   Regular Users:")
    print("     Email: john@example.com")
    print("     Password: password123")
    print("\n     Email: jane@example.com")
    print("     Password: password123")
    print("\n" + "="*60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_database())
