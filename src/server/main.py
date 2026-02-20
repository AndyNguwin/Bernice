from fastapi import FastAPI
from .routes.interactions import router as interactions_router

app = FastAPI()

app.include_router(interactions_router)