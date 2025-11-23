from fastapi import APIRouter, HTTPException, status, Query, Depends
from datetime import datetime
from bson import ObjectId
import math
from app.schemas.order import OrderResponse, OrderCreate, OrderList, OrderStatus, OrderItemBase
from app.api.deps import get_current_active_user
from app.core.database import get_database
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Create a new order"""
    user_id = str(current_user.id)
    
    # Get user's cart
    cart = await db.carts.find_one({"user_id": user_id})
    if not cart or not cart.get("items"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Prepare order items and calculate total
    order_items = []
    total = 0.0
    
    for item in cart["items"]:
        product = await db.products.find_one({"_id": ObjectId(item["product_id"])})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item['product_id']} not found"
            )
        
        if product["stock"] < item["quantity"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product['name']}"
            )
        
        subtotal = product["price"] * item["quantity"]
        order_items.append(OrderItemBase(
            product_id=str(product["_id"]),
            product_name=product["name"],
            quantity=item["quantity"],
            price=product["price"],
            subtotal=subtotal
        ))
        total += subtotal
        
        # Update product stock
        await db.products.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": -item["quantity"]}}
        )
    
    # Create order
    new_order = {
        "user_id": user_id,
        "items": [item.model_dump() for item in order_items],
        "total": total,
        "status": OrderStatus.PENDING,
        "shipping_address": order_data.shipping_address.model_dump(),
        "payment_method": order_data.payment_method,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.orders.insert_one(new_order)
    new_order["id"] = str(result.inserted_id)
    
    # Clear cart
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": {"items": [], "updated_at": datetime.utcnow()}}
    )
    
    return OrderResponse(**new_order)

@router.get("/", response_model=OrderList)
async def get_user_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get user's order history"""
    user_id = str(current_user.id)
    
    # Get total count
    total = await db.orders.count_documents({"user_id": user_id})
    
    # Calculate pagination
    skip = (page - 1) * limit
    pages = math.ceil(total / limit)
    
    # Get orders
    cursor = db.orders.find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
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

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get order by ID"""
    try:
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Verify order belongs to user (unless admin)
    if order["user_id"] != str(current_user.id) and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )
    
    order["id"] = str(order["_id"])
    return OrderResponse(**order)

@router.put("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: str,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Cancel an order"""
    try:
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Verify order belongs to user
    if order["user_id"] != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this order"
        )
    
    # Check if order can be cancelled
    if order["status"] in [OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order with status {order['status']}"
        )
    
    # Restore product stock
    for item in order["items"]:
        await db.products.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": item["quantity"]}}
        )
    
    # Update order status
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": OrderStatus.CANCELLED, "updated_at": datetime.utcnow()}}
    )
    
    # Get updated order
    updated_order = await db.orders.find_one({"_id": ObjectId(order_id)})
    updated_order["id"] = str(updated_order["_id"])
    
    return OrderResponse(**updated_order)

@router.get("/{order_id}/status")
async def get_order_status(
    order_id: str,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get order status"""
    try:
        order = await db.orders.find_one({"_id": ObjectId(order_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Verify order belongs to user
    if order["user_id"] != str(current_user.id) and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order"
        )
    
    return {
        "order_id": str(order["_id"]),
        "status": order["status"],
        "created_at": order["created_at"],
        "updated_at": order["updated_at"]
    }
