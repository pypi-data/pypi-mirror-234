from typing import Optional
from axsqlalchemy.schema import BaseModel


class Organization(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class EmployeeSchema(BaseModel):
    name: str
    role: Optional[str] = None
    organization_id: int

