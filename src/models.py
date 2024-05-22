
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields


class Employee(Model):
    full_name = fields.CharField(max_length=255)
    login = fields.CharField(max_length=50)
    password = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100, null=True)
    subdivision = fields.ForeignKeyField('models.Subdivision', on_delete=fields.CASCADE)

    def __str__(self):
        return self.full_name


class Event(Model):
    employee = fields.ForeignKeyField('models.Employee', on_delete=fields.CASCADE)
    begin = fields.DateField()
    end = fields.DateField()
    description = fields.TextField()

    def __str__(self):
        return self.description


class Subdivision(Model):
    name = fields.CharField(max_length=255)
    leader = fields.IntField()

    def __str__(self):
        return self.name


employee_pydantic = pydantic_model_creator(Employee)
employee_pydantic_no_ids = pydantic_model_creator(Employee, exclude_readonly=True)

subdivision_pydantic = pydantic_model_creator(Subdivision)
subdivision_pydantic_no_ids = pydantic_model_creator(Subdivision, exclude_readonly=True)

event_pydantic = pydantic_model_creator(Event)
event_pydantic_no_ids = pydantic_model_creator(Event, exclude_readonly=True)
