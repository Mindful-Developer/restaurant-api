import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers import menu_controller, order_controller

load_dotenv()

# print(os.environ)
app = FastAPI(title="Restaurant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(menu_controller.router)
app.include_router(order_controller.router)

@app.get("/")
async def root():
    return {"message": "Restaurant API is running"}