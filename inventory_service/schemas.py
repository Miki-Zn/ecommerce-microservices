from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    price: float
    quantity_in_stock: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True 