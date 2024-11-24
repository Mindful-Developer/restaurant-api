from pydantic import BaseModel, condecimal
from typing import Optional, List
from datetime import datetime

from api.models.menu_item import MenuItem

class OrderItem(BaseModel):
    item: MenuItem
    quantity: int

class Order(BaseModel):
    order_number: str
    items: List[MenuItem]
    subtotal: float
    total: float
    discount_pct: float
    order_date: datetime = datetime.now()