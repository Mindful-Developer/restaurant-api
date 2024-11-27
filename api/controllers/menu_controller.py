from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from ..repositories.menu_repository import MenuRepository
from ..schemas.menu_schemas import MenuItemCreate, MenuItemResponse, MenuItemUpdate

router = APIRouter(prefix="/menu", tags=["menu"])

menu_repository = MenuRepository()


@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
async def create_menu_item(item: MenuItemCreate):
    """Create a new menu item"""
    try:
        item_dict = item.model_dump()
        item_dict['created_at'] = str(datetime.now().timestamp())
        item_dict['price'] = Decimal(str(item_dict['price']))

        created_item = await menu_repository.create_item(item_dict)
        return created_item
    except Exception as e:
        print(f"Error in create_menu_item: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[MenuItemResponse])
async def get_all_menu_items():
    """Get all menu items"""
    try:
        items = await menu_repository.get_all()
        for i, item in enumerate(items):
            for attr, val in item.items():
                if attr == 'price':
                    items[i][attr] = float(val)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: str):
    """Get a specific menu item by ID"""
    try:
        item = await menu_repository.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")
        for attr, val in item.items():
            if attr == 'price':
                item[attr] = float(val)
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(item_id: str, item: MenuItemCreate):
    """Update an entire menu item"""
    try:
        existing_item = await menu_repository.get_by_id(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Menu item not found")

        item_dict = item.model_dump()
        item_dict['created_at'] = str(datetime.now().timestamp())
        updated_item = await menu_repository.update_item(item_id, item_dict)
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{item_id}", response_model=MenuItemResponse)
async def patch_menu_item(item_id: str, item: MenuItemUpdate):
    """Partially update a menu item"""
    try:
        existing_item = await menu_repository.get_by_id(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Menu item not found")

        item_dict = item.model_dump(exclude_unset=True)
        item_dict['created_at'] = str(datetime.now().timestamp())
        patched_item = await menu_repository.patch_item(item_id, item_dict)
        return patched_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(item_id: str):
    """Delete a menu item"""
    try:
        existing_item = await menu_repository.get_by_id(item_id)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Menu item not found")

        await menu_repository.delete_item(item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))