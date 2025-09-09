# crud.py
# Import models, schemas, and necessary utilities.
from sqlalchemy.orm import Session, joinedload
import models, schemas
from passlib.context import CryptContext  # Add this import

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Inline get_password_hash function
def get_password_hash(password: str):
    return pwd_context.hash(password)

# User CRUD.
def create_user(db: Session, user: schemas.UserCreate):
    # Check if group exists, create if not.
    group = db.query(models.Group).filter(models.Group.name == user.group_name).first()
    if not group:
        group = models.Group(name=user.group_name)
        db.add(group)
        db.commit()
        db.refresh(group)
    # Create user with hashed password.
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db_user.groups.append(group)  # Add the group.
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Department CRUD.
def create_department(db: Session, department: schemas.DepartmentCreate):
    db_dept = models.Department(**department.dict())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

def get_departments(db: Session):
    return db.query(models.Department).all()

# Employee CRUD.
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_emp = models.Employee(**employee.model_dump())
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    # Load department relation.
    db.refresh(db_emp)
    return db_emp

def get_employees(db: Session):
    # Use joinedload to eagerly load the Department relation.
    return db.query(models.Employee).options(joinedload(models.Employee.Department)).all()

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).options(joinedload(models.Employee.Department)).filter(models.Employee.EmployeeId == employee_id).first()

def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeUpdate):
    db_emp = get_employee(db, employee_id)
    if not db_emp:
        return None
    update_data = employee.dict(exclude_unset=True)  # Only update provided fields.
    for key, value in update_data.items():
        setattr(db_emp, key, value)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def delete_employee(db: Session, employee_id: int):
    db_emp = get_employee(db, employee_id)
    if db_emp:
        db.delete(db_emp)
        db.commit()
    return db_emp