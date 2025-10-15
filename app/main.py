from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.v1 import auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User & Movie API")

# Include versioned API routers
app.include_router(auth.router, prefix="/api/v1", tags=["Auth & Users"])
