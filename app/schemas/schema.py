from pydantic import BaseModel
from typing import Optional

class BiodataCreate(BaseModel):
    name: str
    email: str
    phone: str
    gender: str
    address: Optional[str] = ""

class BiodataResponse(BiodataCreate):
    id: int
    created_at: str

    class Config:
        from_attributes = True