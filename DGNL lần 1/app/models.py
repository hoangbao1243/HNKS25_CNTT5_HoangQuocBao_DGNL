from pydantic import BaseModel, Field
from typing import Optional, Any

class CourseCreate(BaseModel):
    course_code: str = Field(..., min_length=4, max_length=10)
    tuition_fee: float = Field(..., gt=0)
    course_category_id: int

class CourseCategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CourseResponse(BaseModel):
    id: int
    course_code: str
    tuition_fee: float
    course_category_id: int
    category: Optional[CourseCategoryResponse] = None

    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    statusCode: int
    error: Optional[str]
    message: str
    data: Any