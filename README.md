# Task Management API

A REST API developed using Python and FastAPI
for managing tasks.

## Technologies

- Python
- FastAPI
- Uvicorn
- Pytest
- Git
- Jenkins
- Docker
- Ansible
- Kubernetes

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Application information |
| GET | /health | Health check |
| GET | /todos | List tasks |
| POST | /todos | Create task |
| GET | /todos/{id} | Retrieve task |

## Run Locally

Install dependencies:

pip install -r requirements.txt

Start application:

uvicorn app.main:app --reload

Open documentation:

http://localhost:8000/docs

## Run Tests

python -m pytest -v
