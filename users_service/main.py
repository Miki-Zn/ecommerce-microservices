from fastapi import FastAPI

app = FastAPI(title="Users Service", version="1.0.0")

@app.get("/")
async def root():
    return {"service": "Users Service", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}