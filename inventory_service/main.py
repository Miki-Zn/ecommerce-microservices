from fastapi import FastAPI

app = FastAPI(title="Inventory Service", version="1.0.0")

@app.get("/")
async def root():
    return {"service": "Inventory Service", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}