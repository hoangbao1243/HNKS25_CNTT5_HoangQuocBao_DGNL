from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class CourseCategory(Base):
    __tablename__ = "course_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    courses = relationship("Course", back_populates="category")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_code = Column(String(10), unique=True, nullable=False)
    tuition_fee = Column(Float, nullable=False)
    course_category_id = Column(Integer, ForeignKey("course_categories.id"))

    category = relationship("CourseCategory", back_populates="courses")