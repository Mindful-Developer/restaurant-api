from fastapi import FastAPI


app = FastAPI(title="Restaurant API")


@app.get("/")
async def root():
    return {"message": "Restaurant API is running"}