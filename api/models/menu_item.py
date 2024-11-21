from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MenuItem(BaseModel):
    item_id: str
    name: str
    price: float
    description: Optional[str] = None
    category: str
    created_at: datetime = datetime.now()