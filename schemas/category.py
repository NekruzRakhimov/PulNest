from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategorySchema(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    deleted_at: Optional[datetime] = None 

    def dict(self):
        data = super().dict()
        if data["created_at"]:
            data["created_at"] = data["created_at"].isoformat()
        if data["deleted_at"]:
            data["deleted_at"] = data["deleted_at"].isoformat()
        return data
    


