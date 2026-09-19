# TeamTask API

A backend REST API for managing projects, project members, and tasks, built with Django REST Framework.

TeamTask provides JWT-based authentication, role-based authorization, project and task management, filtering, searching, pagination, automated testing, PostgreSQL, and Docker-based development/deployment.

## Features

* JWT authentication

  * Login
  * Access token refresh
  * Logout with token blacklisting
  * Authenticated user profile
* User registration
* Role-based project authorization

  * Owner
  * Admin
  * Member
* Project management

  * Create projects
  * View projects
  * Update projects
  * Delete projects
* Project member management
* Task management

  * Create tasks
  * View tasks
  * Update tasks
  * Delete tasks
  * Assign tasks to project members
  * Task status and priority
  * Due dates
* Filtering
* Search
* Ordering
* Pagination
* Request validation
* Automated API tests
* Test coverage
* PostgreSQL database
* Docker and Docker Compose
* Gunicorn production WSGI server
* OpenAPI / Swagger documentation

## Tech Stack

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python                | Programming language            |
| Django                | Backend framework               |
| Django REST Framework | REST API development            |
| Simple JWT            | JWT authentication              |
| PostgreSQL            | Database                        |
| Docker                | Containerization                |
| Docker Compose        | Multi-container development     |
| Gunicorn              | WSGI server                     |
| drf-spectacular       | OpenAPI / Swagger documentation |
| django-filter         | API filtering                   |

## Project Structure

```text
TeamTask-API/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── project/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── tasks/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── serializer.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── staticfiles/
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```


## Authentication

TeamTask uses JWT authentication.

### Authentication flow

```text
Register
   ↓
Login
   ↓
Access Token + Refresh Token
   ↓
Authenticated API Requests
   ↓
Access Token expires
   ↓
Refresh Token
   ↓
New Access Token
```

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

Logout uses JWT token blacklisting to invalidate the refresh token.

## Authorization

Project access is controlled using project membership and roles.

### Owner

The project owner has the highest level of project control.

### Admin

Project administrators can perform administrative operations allowed by the API.

### Member

Members can access project resources according to their permissions.

Authorization checks ar
