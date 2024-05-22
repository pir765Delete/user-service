
from fastapi import APIRouter, HTTPException
from models import Subdivision, subdivision_pydantic, subdivision_pydantic_no_ids
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

router = APIRouter(
    tags=["Subdivision"]
)


class Status(BaseModel):
    message: str


@router.post("/create", status_code=201, tags=["Subdivision"])
async def create_subdivision(name: str, leader_id: int):
    subdivision = await Subdivision.create(name=name, leader=leader_id)
    return await subdivision_pydantic.from_tortoise_orm(subdivision)


@router.get("/{subdivision_id}", tags=["Subdivision"],
            response_model=subdivision_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_subdivision(subdivision_id: int):
    return await subdivision_pydantic.from_queryset_single(Subdivision.get(id=subdivision_id))


@router.get("/all", tags=["Subdivision"])
async def get_subdivisions():
    return await subdivision_pydantic.from_queryset(Subdivision.all())


@router.put("/{subdivision_id}", tags=["Subdivision"], response_model=subdivision_pydantic,
            responses={404: {"model": HTTPNotFoundError}})
async def update_subdivision(subdivision_id: int, name: str, leader_id: int):
    await Subdivision.filter(id=subdivision_id).update(name=name, leader=leader_id)
    return await subdivision_pydantic_no_ids.from_queryset_single(Subdivision.get(id=subdivision_id))


@router.delete("/{subdivision_id}", tags=["Subdivision"], response_model=Status,
               responses={404: {"model": HTTPNotFoundError}})
async def delete_subdivision(subdivision_id: int):
    delete_subdivision = await Subdivision.filter(id=subdivision_id).delete()
    if not delete_subdivision:
        raise HTTPException(status_code=404, detail=f"Subdivision {subdivision_id} not found")
    return Status(message=f"Delete subdivision {subdivision_id}")
