"""
Pydantic Models
Define data models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    """Base model for Item"""
    name: str = Field(..., max_length=100, description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    price: float = Field(..., gt=0, description="Item price (must be positive)")
    quantity: int = Field(..., ge=0, description="Item quantity (must be non-negative)")

class Item(ItemBase):
    """Complete Item model with ID and timestamp"""
    id: int = Field(..., description="Item ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True  # For ORM compatibility

class ItemResponse(BaseModel):
    """Response model for item operations"""
    success: bool
    message: str
    data: Optional[Item] = None
