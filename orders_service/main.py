from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db
from rabbitmq import publish_order_created_event 

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orders Service", version="1.0.0")

@app.post("/orders/", response_model=schemas.OrderResponse, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    new_order = models.Order(**order.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    event_data = {
        "order_id": new_order.id,
        "product_id": new_order.product_id,
        "quantity": new_order.quantity,
        "user_id": new_order.user_id
    }
    
    try:
        publish_order_created_event(event_data)
    except Exception as e:
        print(f"Failed to publish message: {e}")

    return new_order