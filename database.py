# create_engine → Creates a connection to the database.
# sessionmaker → Creates database sessions for executing queries.
# declarative_base → Defines a base class for SQLAlchemy ORM models.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# sqlite:/// → Means the database file is in the current directory.
DATABASE_URL = "sqlite:///./books.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()