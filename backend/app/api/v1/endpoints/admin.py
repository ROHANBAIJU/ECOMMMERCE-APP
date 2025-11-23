from fastapi import APIRouter, HTTPException, status, Query, Depends
from datetime import datetime
from bson import ObjectId
import math
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.order import OrderList, OrderResponse, OrderStatus
from app.schemas.user import UserList, UserResponse
from app.api.deps import get_current_admin_user
from app.core.database import get_database
from app.models.user import User

router = APIRouter()

# Product Management
@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    current_user: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Create a new product (Admin only)"""
    new_product = product.model_dump()
    new_product["created_at"] = datetime.utcnow()
    new_product["updated_at"] = datetime.utcnow()
    
    result = await db.products.insert_one(new_product)
    new_product["id"] = str(result.inserted_id)
    
    return ProductResponse(**new_product)

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Update a product (Admin only)"""
    update_data = product_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_data["updated_at"] = datetime.utcnow()
    
    try:
        result = await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Get updated product
    updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
    updated_product["id"] = str(updated_product["_id"])
    
    return ProductResponse(**updated_product)

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    current_user: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Delete a product (Admin only)"""
    try:
        result = await db.products.delete_one({"_id": ObjectId(product_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return {"message": "Product deleted successfully"}

# Order Management
@router.get("/orders", response_model=OrderList)
async def get_all_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    order_status: OrderStatus = None,
    current_user: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Get all orders (Admin only)"""
    query_filter = {}
    if order_status:
        query_filter["status"] = order_status
    
    # Get total count
    total = await db.orders.count_documents(query_filter)
    
    # Calculate pagination
    skip = (page - 1) * limit
    pages = math.ceil(total / limit)
    
    # Get orders
    cursor = db.orders.find(query_filter).sort("created_at", -1).skip(skip).limit(limit)
    orders = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for order in orders:
        order["id"] = str(order["_id"])
    
    return OrderList(
        orders=[OrderResponse(**o) for o in orders],
        total=total,
        page=page,
        pages=pages
    )

@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: str,
    new_status: OrderStatus,
    current_user: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Update order status (Admin only)"""
    try:
        result = await db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return {"message": "Order status updated successfully", "new_status": new_status}

# User Management
@router.get("/users", response_model=UserList)
async def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Get all users (Admin only)"""
    # Get total count
    total = await db.users.count_documents({})
    
    # Calculate pagination
    skip = (page - 1) * limit
    pages = math.ceil(total / limit)
    
    # Get users
    cursor = db.users.find({}).sort("created_at", -1).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string and remove password
    for user in users:
        user["id"] = str(user["_id"])
        user.pop("hashed_password", None)
    
    return UserList(
        users=[UserResponse(**u) for u in users],
        total=total,
        page=page,
        pages=pages
    )

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Delete a user (Admin only)"""
    # Prevent self-deletion
    if user_id == str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    try:
        result = await db.users.delete_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Also delete user's cart and orders (optional, depending on business logic)
    await db.carts.delete_many({"user_id": user_id})
    
    return {"message": "User deleted successfully"}

# Analytics
@router.get("/analytics/dashboard")
async def get_dashboard_analytics(
    current_user: User = Depends(get_current_admin_user),
    db = Depends(get_database)
):
    """Get dashboard analytics (Admin only)"""
    # Get counts
    total_users = await db.users.count_documents({})
    total_products = await db.products.count_documents({})
    total_orders = await db.orders.count_documents({})
    
    # Get order statistics
    pending_orders = await db.orders.count_documents({"status": OrderStatus.PENDING})
    processing_orders = await db.orders.count_documents({"status": OrderStatus.PROCESSING})
    shipped_orders = await db.orders.count_documents({"status": OrderStatus.SHIPPED})
    delivered_orders = await db.orders.count_documents({"status": OrderStatus.DELIVERED})
    cancelled_orders = await db.orders.count_documents({"status": OrderStatus.CANCELLED})
    
    # Calculate total revenue
    orders = await db.orders.find(
        {"status": {"$in": [OrderStatus.PROCESSING, OrderStatus.SHIPPED, OrderStatus.DELIVERED]}}
    ).to_list(length=None)
    total_revenue = sum(order.get("total", 0) for order in orders)
    
    # Get low stock products
    low_stock_products = await db.products.find({"stock": {"$lt": 10}}).to_list(length=10)
    
    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "order_statistics": {
            "pending": pending_orders,
            "processing": processing_orders,
            "shipped": shipped_orders,
            "delivered": delivered_orders,
            "cancelled": cancelled_orders
        },
        "total_revenue": total_revenue,
        "low_stock_products": len(low_stock_products),
        "low_stock_items": [
            {
                "id": str(p["_id"]),
                "name": p["name"],
                "stock": p["stock"]
            }
            for p in low_stock_products
        ]
    }
