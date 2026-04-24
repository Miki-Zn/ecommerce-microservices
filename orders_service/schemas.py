from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_price: float

class OrderResponse(OrderCreate):
    id: int
    status: str

    class Config:
        from_attributes = True