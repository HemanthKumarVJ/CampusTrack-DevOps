
from datetime import date
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="CampusTrack - Student Attendance API",
    description="REST API for student registration and attendance tracking",
    version="1.0.0"
)

students = {}
attendance_records = []
next_student_id = 1


# Request models

class StudentCreate(BaseModel):
    name: str
    roll_number: str
    section: str


class AttendanceCreate(BaseModel):
    student_id: int
    attendance_date: date
    status: Literal["present", "absent"]


# Home endpoint

@app.get("/")
def home():
    return {
        "message": "Welcome to CampusTrack",
        "documentation": "/docs"
    }


# Health check endpoint

@app.get("/health")
def health():
    return {"status": "ok"}


# Register a new student

@app.post("/students", status_code=201)
def register_student(student: StudentCreate):
    global next_student_id

    for existing in students.values():
        if existing["roll_number"] == student.roll_number:
            raise HTTPException(
                status_code=409,
                detail="Roll number already exists"
            )

    new_student = {
        "id": next_student_id,
        "name": student.name,
        "roll_number": student.roll_number,
        "section": student.section
    }

    students[next_student_id] = new_student
    next_student_id += 1

    return new_student


# Get all students

@app.get("/students")
def get_students():
    return list(students.values())


# Search student by roll number

@app.get("/students/roll/{roll_number}")
def get_student_by_roll(roll_number: str):
    for student in students.values():
        if student["roll_number"] == roll_number:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


# Mark student attendance

@app.post("/attendance", status_code=201)
def mark_attendance(record: AttendanceCreate):
    if record.student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    for existing in attendance_records:
        if (
            existing["student_id"] == record.student_id
            and existing["attendance_date"] == record.attendance_date.isoformat()
        ):
            raise HTTPException(
                status_code=409,
                detail="Attendance already marked"
            )

    new_record = {
        "student_id": record.student_id,
        "attendance_date": record.attendance_date.isoformat(),
        "status": record.status
    }

    attendance_records.append(new_record)

    return new_record


# Get attendance records for a student

@app.get("/attendance/{student_id}")
def get_attendance(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return [
        record for record in attendance_records
        if record["student_id"] == student_id
    ]


# Calculate attendance percentage

@app.get("/students/{student_id}/percentage")
def attendance_percentage(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    records = [
        record for record in attendance_records
        if record["student_id"] == student_id
    ]

    total = len(records)

    present = sum(
        record["status"] == "present"
        for record in records
    )

    percentage = round(
        present / total * 100, 2
    ) if total else 0

    return {
        "student_id": student_id,
        "total_classes": total,
        "present": present,
        "absent": total - present,
        "attendance_percentage": percentage
    }

