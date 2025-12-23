from fastapi import FastAPI
from database import engine, Base
import models
from cities.routes import router as city_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(city_router, prefix="/api/v1/cities", tags=["cities"])
