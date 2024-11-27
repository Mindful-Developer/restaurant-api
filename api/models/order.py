from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

from api.models.menu_item import MenuItem

class OrderItem(BaseModel):
    item: MenuItem
    quantity: int

class Order(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            float: lambda v: round(v, 2)
        }
    )
    order_id: str
    order_number: str
    items: List[MenuItem]
    subtotal: float
    total: float
    discount_pct: float
    order_date: str = str(datetime.now().timestamp())