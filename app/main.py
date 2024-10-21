from fastapi import FastAPI
from app.api import endpoints
from app.database import create_tables

app = FastAPI()

# Create tables if not exits on startup
create_tables()

# Include API routes
app.include_router(endpoints.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)