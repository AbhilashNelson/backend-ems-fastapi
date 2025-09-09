# database.py
# Import necessary modules from SQLAlchemy for database engine, session, and base class.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL. Here, we're using SQLite with a local file 'ems.db'.
# 'check_same_thread=False' allows usage in multi-threaded environments like FastAPI.
SQLALCHEMY_DATABASE_URL = "sqlite:///./ems.db"

# Create the database engine, which handles connections to the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory. Local sessions will be created from this.
# 'autocommit=False' means changes aren't saved until explicitly committed.
# 'autoflush=False' means changes aren't automatically flushed to the DB.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models. All SQLAlchemy models will inherit from this.
Base = declarative_base()

# Dependency to get a DB session for each request. This ensures the session is closed after use.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()