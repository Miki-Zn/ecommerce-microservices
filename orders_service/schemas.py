from pydantic import BaseModel

class OrderCreate(BaseModel):
    product_id: int
    quantity: int
    total_price: float

class OrderResponse(OrderCreate):
    id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True