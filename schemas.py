# Import Pydantic's BaseModel for creating schemas.
from pydantic import BaseModel
from typing import List, Optional

# Group schema for responses.
class Group(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True  # Allows creating from ORM objects.

# User schemas.
class UserCreate(BaseModel):  # For signup request.
    username: str
    password: str
    group_name: str  # As per spec, single group name during signup.

class User(BaseModel):  # For responses.
    id: int
    username: str
    groups: List[Group]
    class Config:
        from_attributes = True

# Token schema for login response.
class Token(BaseModel):
    access_token: str
    token_type: str

# Department schemas.
class DepartmentCreate(BaseModel):
    DepartmentName: str

class Department(BaseModel):
    DepartmentId: int
    DepartmentName: str
    class Config:
        from_attributes = True

# Employee schemas.
class EmployeeCreate(BaseModel):
    EmployeeName: str
    Designation: str
    DateOfJoining: str
    Contact: str
    IsActive: bool
    DepartmentId: int

class EmployeeUpdate(BaseModel):
    EmployeeName: Optional[str] = None
    Designation: Optional[str] = None
    DateOfJoining: Optional[str] = None
    Contact: Optional[str] = None
    IsActive: Optional[bool] = None
    DepartmentId: Optional[int] = None

class Employee(BaseModel):
    EmployeeId: int
    EmployeeName: str
    Designation: str
    DateOfJoining: str
    Contact: str
    IsActive: bool
    DepartmentId: int
    Department: Department  # Nested department details.
    class Config:
        from_attributes = True