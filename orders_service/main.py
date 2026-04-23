from fastapi import FastAPI
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orders Service", version="1.0.0")

@app.get("/")
async def root():
    return {"service": "Orders Service", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}