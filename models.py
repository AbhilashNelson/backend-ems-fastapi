# models.py
# Import SQLAlchemy types and relationship utilities.
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

# Import the Base from database.py.
from database import Base

# Association table for many-to-many relationship between Users and Groups.
user_groups = Table(
    'user_groups', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)

# Group model: Represents user groups (e.g., roles like "admin").
class Group(Base):
    __tablename__ = "groups"  # Table name in the database.

    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing primary key.
    name = Column(String, unique=True, index=True)  # Group name, must be unique.

    # Relationship: A group can have many users.
    users = relationship("User", secondary=user_groups, back_populates="groups")

# User model: For authentication.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # Unique username.
    hashed_password = Column(String)  # Stored hashed password (never plain text).

    # Relationship: A user can belong to many groups.
    groups = relationship("Group", secondary=user_groups, back_populates="users")

# Department model.
class Department(Base):
    __tablename__ = "departments"

    DepartmentId = Column(Integer, primary_key=True, index=True)  # Note: Matching exact casing from spec.
    DepartmentName = Column(String, index=True)

    # Relationship: A department can have many employees.
    employees = relationship("Employee", back_populates="Department")

# Employee model.
class Employee(Base):
    __tablename__ = "employees"

    EmployeeId = Column(Integer, primary_key=True, index=True)
    EmployeeName = Column(String, index=True)
    Designation = Column(String)
    DateOfJoining = Column(String)  # Stored as string (YYYY-MM-DD).
    Contact = Column(String)
    IsActive = Column(Boolean, default=True)
    DepartmentId = Column(Integer, ForeignKey("departments.DepartmentId"))

    # Relationship: An employee belongs to one department.
    Department = relationship("Department", back_populates="employees")