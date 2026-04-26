from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import threading

import models
import schemas
from database import engine, get_db
from consumer import start_consuming

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Service", version="1.0.0")

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=start_consuming, daemon=True)
    thread.start()

@app.post("/products/", response_model=schemas.ProductResponse, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[schemas.ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products