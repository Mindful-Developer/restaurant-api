from fastapi import FastAPI
from .controllers import menu_controller, order_controller
app = FastAPI(title="Restaurant API")

# Routers
app.include_router(menu_controller.router)
app.include_router(order_controller.router)
@app.get("/")
async def root():
    return {"message": "Restaurant API is running"}