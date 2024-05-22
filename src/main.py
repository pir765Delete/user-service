
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from database import connectToDatabase
from routers.employees import router as router_employee
from routers.events import router as router_event
from routers.subdivisions import router as router_subdivision


app = FastAPI()


app.include_router(
    router=router_employee,
    prefix="/employee",
    tags=["Employee"]
)

app.include_router(
    router=router_event,
    prefix="/event",
    tags=["Event"]
)

app.include_router(
    router=router_subdivision,
    prefix="/subdivision",
    tags=["Subdivision"]
)


@app.get("/")
async def read_root():
    await connectToDatabase()
    return {"Hello": "world"}


register_tortoise(
    app,
    db_url='postgres://postgres:8s8wxa@localhost:5433/user_service_db',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
