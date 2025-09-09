# This ties everything together: defines the app, endpoints, and dependencies.
# Import FastAPI and necessary components.
from fastapi import FastAPI, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
import crud, schemas, auth
from database import get_db, engine, Base
from datetime import timedelta
#import CORSMiddleware to enable the corss resource access for our react frontend
#Make sure to diable cors once the project is live in the production server
from fastapi.middleware.cors import CORSMiddleware

# Create all tables if not exists (run once).
Base.metadata.create_all(bind=engine)

# Create the FastAPI app.
app = FastAPI()

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #allow access from all origin ip address/domains
    allow_credentials=True,
    allow_methods=["*"], #allow all http methods (get, post etc)
    allow_headers=["*"], #allow all http headers
)

# Root endpoint.
@app.get("/")
def read_root():
    return {"message": "Welcome to EMS FastAPI"}

# Signup endpoint.
@app.post("/auth/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

# Token (login) endpoint. Uses form data.
@app.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Create department (requires auth).
@app.post("/departments/", response_model=schemas.Department)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_department(db, department)

# List departments (no auth required as per spec).
@app.get("/departments/", response_model=list[schemas.Department])
def read_departments(db: Session = Depends(get_db)):
    return crud.get_departments(db)

# Create employee (requires auth).
@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_employee(db, employee)

# List employees.
@app.get("/employees/", response_model=list[schemas.Employee])
def read_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)

# Get single employee.
@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# Update employee (requires auth, but spec doesn't show auth for update; adding for consistency).
@app.put("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    updated_employee = crud.update_employee(db, employee_id, employee)
    if updated_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee

# Delete employee (requires auth).
@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    deleted = crud.delete_employee(db, employee_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None  # 204 No Content