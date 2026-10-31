import re

def clean_and_validate_courses(courses):
    valid_courses = []
    for course in courses:
        c = course.copy()
        code = str(c.get("course_code", "")).strip().upper()
        c["course_code"] = code

        if re.match(r"^K\d+$", code):
            valid_courses.append(c)

    return valid_courses

def search_courses(courses, max_fee, status=None):
    result = []
    for course in courses:
        fee = course.get("tuition_fee", 0)
        course_status = course.get("status")

        if fee <= max_fee:
            if status is None or course_status == status:
                result.append(course)

    return result

def sort_courses_by_tuition_fee_desc(courses):
    arr = courses.copy()
    n = len(arr)

    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j].get("tuition_fee", 0) < arr[j + 1].get("tuition_fee", 0):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr

if __name__ == "__main__":
    raw_courses = [
        {"course_code": "K301", "category": "programming", "tuition_fee": 4500000, "status": "open"},
        {"course_code": "k101 ", "category": "design", "tuition_fee": 2800000, "status": "open"},
        {"course_code": "K202", "category": "marketing", "tuition_fee": 3200000, "status": "full"},
        {"course_code": "K102", "category": "design", "tuition_fee": 2500000, "status": "closed"},
        {"course_code": "K302", "category": "programming", "tuition_fee": 5200000, "status": "open"},
        {"course_code": "A105", "category": "design", "tuition_fee": 2000000, "status": "open"}
    ]

    cleaned_courses = clean_and_validate_courses(raw_courses)
    print("1. Cleaned and Validated Courses:")
    for c in cleaned_courses:
        print(c)
    print("-" * 50)

    searched_courses = search_courses(cleaned_courses, 4000000, "open")
    print("2. Searched Courses (fee <= 4,000,000 and status == 'open'):")
    for c in searched_courses:
        print(c)
    print("-" * 50)

    sorted_courses = sort_courses_by_tuition_fee_desc(cleaned_courses)
    print("3. Sorted Courses by Tuition Fee (Descending):")
    for c in sorted_courses:
        print(c)