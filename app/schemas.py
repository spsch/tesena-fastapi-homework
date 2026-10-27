from typing import Optional
from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(..., example="Test card")
    description: Optional[str] = Field(None, example="Card for E2E tests")
    price: float = Field(..., gt=0, example=150.0)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated card")
    description: Optional[str] = Field(None)
    price: Optional[float] = Field(None, gt=0)

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True