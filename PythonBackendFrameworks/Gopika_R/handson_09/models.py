from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class User(Base):
    """
    User DB Model (Task 1 - Step 86)
    Fields: id, email (unique), hashed_password, is_active
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Course(Base):
    """
    Course DB Model
    Used for testing protected endpoints (POST/DELETE courses).
    """
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    code = Column(String, nullable=False)
    department = Column(String, nullable=False)
    credits = Column(Integer, default=3)
