from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import Optional
from bson import ObjectId
import math
from app.schemas.product import ProductResponse, ProductList
from app.core.database import get_database

router = APIRouter()

@router.get("/", response_model=ProductList)
async def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = Query(None, regex="^(price|name|created_at)$"),
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    db = Depends(get_database)
):
    """Get products with filters and pagination"""
    # Build query
    query_filter = {}
    
    if category:
        query_filter["category"] = category
    
    if search:
        query_filter["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        query_filter["price"] = price_filter
    
    # Get total count
    total = await db.products.count_documents(query_filter)
    
    # Calculate pagination
    skip = (page - 1) * limit
    pages = math.ceil(total / limit)
    
    # Build sort
    sort_field = sort_by or "created_at"
    sort_direction = 1 if sort_order == "asc" else -1
    
    # Get products
    cursor = db.products.find(query_filter).sort(sort_field, sort_direction).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for product in products:
        product["id"] = str(product["_id"])
    
    return ProductList(
        products=[ProductResponse(**p) for p in products],
        total=total,
        page=page,
        pages=pages
    )

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db = Depends(get_database)):
    """Get product by ID"""
    try:
        product = await db.products.find_one({"_id": ObjectId(product_id)})
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
    
    product["id"] = str(product["_id"])
    return ProductResponse(**product)

@router.get("/category/{category_name}", response_model=ProductList)
async def get_products_by_category(
    category_name: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db = Depends(get_database)
):
    """Get products by category"""
    return await get_products(
        page=page,
        limit=limit,
        category=category_name,
        db=db
    )

@router.get("/search/{query}", response_model=ProductList)
async def search_products(
    query: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db = Depends(get_database)
):
    """Search products"""
    return await get_products(
        page=page,
        limit=limit,
        search=query,
        db=db
    )
