from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from bson import ObjectId
from typing import List
from app.schemas.cart import CartResponse, CartItemAdd, CartItemUpdate, CartItem
from app.api.deps import get_current_active_user
from app.core.database import get_database
from app.models.user import User

router = APIRouter()

async def get_cart_with_details(user_id: str, db):
    """Helper function to get cart with product details"""
    cart = await db.carts.find_one({"user_id": user_id})
    
    if not cart:
        # Create new cart
        cart = {
            "user_id": user_id,
            "items": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        await db.carts.insert_one(cart)
    
    cart_items = []
    total = 0.0
    
    for item in cart.get("items", []):
        product = await db.products.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            subtotal = product["price"] * item["quantity"]
            cart_items.append(CartItem(
                id=str(item["product_id"]),
                product_id=str(item["product_id"]),
                product_name=product["name"],
                product_price=product["price"],
                product_image=product["images"][0] if product["images"] else "",
                quantity=item["quantity"],
                subtotal=subtotal
            ))
            total += subtotal
    
    return CartResponse(
        user_id=user_id,
        items=cart_items,
        total=total,
        item_count=len(cart_items),
        updated_at=cart.get("updated_at", datetime.utcnow())
    )

@router.get("/", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get user's shopping cart"""
    return await get_cart_with_details(str(current_user.id), db)

@router.post("/items", response_model=CartResponse)
async def add_to_cart(
    item: CartItemAdd,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Add item to cart"""
    # Verify product exists and has stock
    try:
        product = await db.products.find_one({"_id": ObjectId(item.product_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if product["stock"] < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )
    
    user_id = str(current_user.id)
    cart = await db.carts.find_one({"user_id": user_id})
    
    if not cart:
        cart = {
            "user_id": user_id,
            "items": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        await db.carts.insert_one(cart)
    
    # Check if item already in cart
    items = cart.get("items", [])
    existing_item = next((i for i in items if i["product_id"] == item.product_id), None)
    
    if existing_item:
        # Update quantity
        new_quantity = existing_item["quantity"] + item.quantity
        if product["stock"] < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )
        existing_item["quantity"] = new_quantity
    else:
        # Add new item
        items.append({
            "product_id": item.product_id,
            "quantity": item.quantity
        })
    
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": {"items": items, "updated_at": datetime.utcnow()}}
    )
    
    return await get_cart_with_details(user_id, db)

@router.put("/items/{item_id}", response_model=CartResponse)
async def update_cart_item(
    item_id: str,
    item_update: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Update cart item quantity"""
    user_id = str(current_user.id)
    cart = await db.carts.find_one({"user_id": user_id})
    
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    items = cart.get("items", [])
    item_to_update = next((i for i in items if i["product_id"] == item_id), None)
    
    if not item_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not in cart"
        )
    
    # Verify stock
    try:
        product = await db.products.find_one({"_id": ObjectId(item_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    if product["stock"] < item_update.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )
    
    item_to_update["quantity"] = item_update.quantity
    
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": {"items": items, "updated_at": datetime.utcnow()}}
    )
    
    return await get_cart_with_details(user_id, db)

@router.delete("/items/{item_id}", response_model=CartResponse)
async def remove_from_cart(
    item_id: str,
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Remove item from cart"""
    user_id = str(current_user.id)
    cart = await db.carts.find_one({"user_id": user_id})
    
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    items = [i for i in cart.get("items", []) if i["product_id"] != item_id]
    
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": {"items": items, "updated_at": datetime.utcnow()}}
    )
    
    return await get_cart_with_details(user_id, db)

@router.delete("/", response_model=dict)
async def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Clear entire cart"""
    user_id = str(current_user.id)
    await db.carts.update_one(
        {"user_id": user_id},
        {"$set": {"items": [], "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Cart cleared successfully"}
