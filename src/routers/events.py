from datetime import date

from fastapi import APIRouter, HTTPException
from models import Event, event_pydantic, event_pydantic_no_ids
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

router = APIRouter(
    tags=["Event"]
)


class Status(BaseModel):
    message: str


@router.post("/create", status_code=201, tags=["Event"])
async def create_event(employee_id: int, begin: date, end: date, description: str):
    if begin > end:
        return Status(message=f'Date entered incorrectly (value begin > end)')
    events = await Event.filter(employee_id=employee_id)
    for event in events:
        if (begin <= event.begin <= end) or (event.end >= begin >= event.begin):
            return Status(message=f'Intersection with another event (check the list of events and try again)')
    event = await Event.create(begin=begin, end=end, description=description, employee_id=employee_id)
    return await event_pydantic.from_tortoise_orm(event)


@router.get("/{event_id}", tags=["Event"], response_model=event_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_event(event_id: int):
    return await event_pydantic.from_queryset_single(Event.get(id=event_id))


@router.get("/all/", tags=["Event"])
async def get_events():
    return await event_pydantic.from_queryset(Event.all())


@router.put("/{event_id}", tags=["Event"], response_model=event_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_event(event_id: int, begin: date, end: date, description: str):
    await Event.filter(id=event_id).update(begin=begin, end=end, description=description)
    return await event_pydantic_no_ids.from_queryset_single(Event.get(id=event_id))


@router.delete("/{event_id}", tags=["Event"], response_model=Status,
               responses={404: {"model": HTTPNotFoundError}})
async def delete_event(event_id: int):
    event_deleted: bool = await Event.filter(id=event_id).delete()
    if not event_deleted:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
    return Status(message=f"Delete event {event_id}")
