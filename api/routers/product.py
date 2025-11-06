from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from schemas.product import ProductOut, ProductFilter, BaseProduct, ProductInsert, ProductFilterBase
from schemas.user import UserOut
from core.dependencies import get_current_user
from services.product_service import product_service

router = APIRouter(prefix='/products', tags=["Products"])

@router.get("/", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_products(current_user : UserOut = Depends(get_current_user)):
    return await product_service.get_products(ProductFilter(user_id=current_user.id))

@router.post("/filter", response_model=List[ProductOut], status_code=status.HTTP_200_OK)
async def get_products(product_filters : ProductFilterBase, current_user : UserOut = Depends(get_current_user)):
    return await product_service.get_products(
        ProductFilter(**product_filters.model_dump(), user_id=current_user.id)
    )

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(product_data : BaseProduct, current_user : UserOut = Depends(get_current_user)):
    product_exists = await product_service.get_products(ProductFilter(user_id=current_user.id, name=product_data.name))
    if product_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Product already exists!!'
        )
    
    product_add = ProductInsert(name=product_data.name, stock=product_data.stock, price=product_data.price, user_id=current_user.id)
    
    new_id = await product_service.insert_product(product_add)
    if not new_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering product."
        )
    
    products = await product_service.get_products(ProductFilter(id=new_id))
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[0]
    
    