from datetime import datetime

from pydantic import BaseModel, condecimal
from typing import Optional

class MenuItemCreate(BaseModel):
    name: str
    price: condecimal(max_digits=10, decimal_places=2)
    description: Optional[str] = None
    category: str

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    price: condecimal(max_digits=10, decimal_places=2) = None
    description: Optional[str] = None
    category: Optional[str] = None

class MenuItemResponse(BaseModel):
    item_id: str
    name: str
    price: condecimal(max_digits=10, decimal_places=2)
    description: Optional[str]
    category: str