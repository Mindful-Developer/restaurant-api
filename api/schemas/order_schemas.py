from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, condecimal, Field, conint
from typing import Optional, List

from api.schemas.menu_schemas import MenuItemResponse

class OrderItem(BaseModel):
    item: MenuItemResponse
    quantity: conint(gt=0, lt=1000)

class OrderCreate(BaseModel):
    order_number: str
    items: List[OrderItem]
    subtotal: Optional[condecimal(max_digits=15, decimal_places=2)] = Decimal(0.00)
    discount_pct: Optional[condecimal(ge=0, le=1, decimal_places=2)] = Decimal(0.00)
    total: Optional[condecimal(max_digits=15, decimal_places=2)] = Decimal(0.00)
    order_date: str = str(datetime.now().timestamp())

class OrderUpdate(BaseModel):
    order_number: Optional[str] = None
    items: Optional[List[OrderItem]] = None
    subtotal: condecimal(max_digits=15, decimal_places=2) = None
    discount_pct: Optional[condecimal(ge=0, le=1, decimal_places=2)] = None
    total: Optional[condecimal(max_digits=15, decimal_places=2)] = None
    order_date: str = None

class OrderResponse(BaseModel):
    order_id: str
    order_number: str
    items: List[OrderItem]
    subtotal: condecimal(max_digits=15, decimal_places=2)
    discount_pct: condecimal(ge=0, le=1, decimal_places=2)
    total: condecimal(max_digits=15, decimal_places=2)
    order_date: str