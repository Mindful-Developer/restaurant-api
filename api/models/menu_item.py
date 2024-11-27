from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MenuItem(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            float: lambda v: round(v, 2)
        }
    )
    item_id: str
    name: str
    price: float
    description: Optional[str] = None
    category: str
    created_at: str = str(datetime.now())