from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/courses", response_model=schemas.APIResponse)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    category = db.query(models.CourseCategory).filter(models.CourseCategory.id == course.course_category_id).first()
    if not category:
        return JSONResponse(
            status_code=404,
            content={"statusCode": 404, "error": "Not Found", "message": "Danh mục khóa học không tồn tại", "data": None}
        )

    existing_course = db.query(models.Course).filter(models.Course.course_code == course.course_code).first()
    if existing_course:
        return JSONResponse(
            status_code=400,
            content={"statusCode": 400, "error": "Bad Request", "message": "Mã khóa học đã tồn tại", "data": None}
        )

    new_course = models.Course(
        course_code=course.course_code,
        tuition_fee=course.tuition_fee,
        course_category_id=course.course_category_id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return JSONResponse(
        status_code=201,
        content={
            "statusCode": 201,
            "error": None,
            "message": "Thêm khóa học thành công",
            "data": schemas.CourseResponse.model_validate(new_course).model_dump()
        }
    )

@app.get("/courses", response_model=schemas.APIResponse)
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    result = [schemas.CourseResponse.model_validate(c).model_dump() for c in courses]

    return {
        "statusCode": 200,
        "error": None,
        "message": "Lấy danh sách khóa học thành công",
        "data": result
    }

@app.delete("/course-categories/{id}", response_model=schemas.APIResponse)
def delete_course_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.CourseCategory).filter(models.CourseCategory.id == id).first()
    if not category:
        return JSONResponse(
            status_code=404,
            content={"statusCode": 404, "error": "Not Found", "message": "Danh mục khóa học không tồn tại", "data": None}
        )

    if category.courses:
        return JSONResponse(
            status_code=400,
            content={"statusCode": 400, "error": "Bad Request", "message": "Không thể xóa danh mục đang có khóa học", "data": None}
        )

    db.delete(category)
    db.commit()

    return {
        "statusCode": 200,
        "error": None,
        "message": "Xóa danh mục khóa học thành công",
    
        "data": None
    }