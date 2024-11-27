from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from typing import List
import uuid

from fastapi import APIRouter, status, Response, HTTPException
from api.repositories.order_repository import OrderRepository
from api.schemas.order_schemas import OrderUpdate, OrderResponse, OrderCreate

def calculate_price(order:dict):
    items = order['items']

    subtotal = Decimal('0.0')
    for item_dict in items:
        item_dict['item']['price'] = Decimal(str(item_dict['item']['price']))
        item_dict['quantity'] = Decimal(str(item_dict['quantity']))
        subtotal += item_dict['item']['price'] * item_dict['quantity']

    order['subtotal'] = subtotal.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    discount = order['subtotal'] * order['discount_pct']
    total = order['subtotal'] - discount
    order['total'] = total.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    return order

router = APIRouter(prefix="/orders", tags=["order"])

order_repository = OrderRepository()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """Create a new order"""
    try:
        order_dict = order.model_dump()

        if not order_dict.get('order_number'):
            order_dict['order_number'] = str(uuid.uuid4())[:6]

        order_dict = calculate_price(order_dict)
        order_dict['order_date'] = str(datetime.now().timestamp())
        created_order = await order_repository.create_order(order_dict)
        return created_order
    except Exception as e:
        print(f"Error in create_order: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[OrderResponse])
async def get_all_orders():
    """Get all order"""
    try:
        orders = await order_repository.get_all()
        for i, order in enumerate(orders):
            for j, item in enumerate(order['items']):
                for attr, val in item.items():
                    if isinstance(val, Decimal):
                        orders[i]['items'][j][attr] = float(val)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    """Get a specific order by ID"""
    try:
        order = await order_repository.get_by_id(order_id)
        for i, item in enumerate(order['items']):
            for attr, val in item.items():
                if isinstance(val, Decimal):
                    order['items'][i][attr] = float(val)
        if not order:
            raise HTTPException(status_code=404, detail="Order order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: str, order: OrderCreate):
    """Update an entire order"""
    try:
        existing_order = await order_repository.get_by_id(order_id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")
        order_dict = order.model_dump()
        order_dict['order_id'] = order_id
        order_dict = calculate_price(order_dict)
        order_dict['order_date'] = str(datetime.now().timestamp())
        updated_order = await order_repository.update_order(order_id, order_dict)
        return updated_order
    except Exception as e:
        print(f"Error in update_order: {str(e)}", flush=True)  # Added logging
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{order_id}", response_model=OrderResponse)
async def patch_order(order_id: str, order: OrderUpdate):
    """Partially update a order"""
    try:
        existing_order = await order_repository.get_by_id(order_id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order order not found")
        order_dict = order.model_dump(exclude_unset=True)
        order_dict = calculate_price(order_dict)
        order_dict["order_date"] = str(datetime.now().timestamp())
        patched_order = await order_repository.patch_order(order_id, order_dict)
        return patched_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str):
    """Delete an order"""
    try:
        existing_order = await order_repository.get_by_id(order_id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")

        await order_repository.delete_order(order_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))