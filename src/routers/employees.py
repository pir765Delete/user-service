from fastapi import APIRouter, HTTPException
from models import employee_pydantic, Employee, employee_pydantic_no_ids
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


class Status(BaseModel):
    message: str


@router.post("/create", status_code=201, tags=["Employee"])
async def create_employee(full_name: str, login: str, password: str, email: str, subdivision_id: int):
    employee = await Employee.create(full_name=full_name, login=login, password=password,
                                     email=email, subdivision_id=subdivision_id)
    return await employee_pydantic.from_tortoise_orm(employee)


@router.get("/{employee_id}", tags=["Employee"], response_model=employee_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_employee(employee_id: int):
    return await employee_pydantic.from_queryset_single(Employee.get(id=employee_id))


@router.get("/all")
async def get_employees():
    return await employee_pydantic.from_queryset(Employee.all())


@router.put("/{employee_id}", tags=["Employee"], response_model=employee_pydantic, responses={404: {"model":HTTPNotFoundError}})
async def update_employee(employee_id: int, full_name: str, login: str, password: str, email: str, subdivision_id: int):
    await Employee.filter(id=employee_id).update(full_name=full_name, login=login,
                                                 password=password, email=email, subdivision_id=subdivision_id)
    return await employee_pydantic_no_ids.from_queryset_single(Employee.get(id=employee_id))


@router.delete("/{employee_id}", tags=["Employee"], response_model=Status,
               responses={404: {"model": HTTPNotFoundError}})
async def delete_employee(employee_id: int):
    delete_employee = await Employee.filter(id=employee_id).delete()
    if not delete_employee:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    return Status(message=f"Delete employee {employee_id}")
