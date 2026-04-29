from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import threading

import json
import redis

import models
import schemas
from database import engine, get_db
from consumer import start_consuming

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Service", version="1.0.0")

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

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

    redis_client.delete("products_list") 
    return db_product

@app.get("/products/", response_model=List[schemas.ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cached_products = redis_client.get("products_list")
    
    if cached_products:
        print("🚀 Taken from Redis cache!")
        return json.loads(cached_products)

    print("🐢 Let's go to the long PostgreSQL database...")
    products = db.query(models.Product).offset(skip).limit(limit).all()
    
    products_data = [schemas.ProductResponse.model_validate(p).model_dump() for p in products]
    redis_client.setex("products_list", 60, json.dumps(products_data))
    
    return products