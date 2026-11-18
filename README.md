
# CampusTrack - Student Attendance Management API

## Project Overview
CampusTrack is a REST API developed using Python and FastAPI to manage student registration and attendance records.

## Features
- Register students
- View registered students
- Mark daily attendance
- View individual attendance records
- Calculate attendance percentage
- Prevent duplicate roll numbers
- Prevent duplicate attendance entries for the same date
- Health monitoring endpoint

## Technologies Used
- Python
- FastAPI
- Uvicorn
- Pytest
- Git and GitHub

## Project Structure
```text
devops-task-api/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── requirements.txt
├── requirements-lock.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd devops-task-api
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API documentation:

http://localhost:8000/docs

## Run Automated Tests

```bash
python -m pytest -v
```

## Project Status
Application development and initial automated testing completed.
DevOps integration and deployment are part of the ongoing project.

Jenkins automatic build trigger verification.
Jenkins automatic build trigger verification.
