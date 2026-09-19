# TeamTask API

A production-oriented REST API for managing projects, project members, and tasks, built with **Django REST Framework**.

TeamTask implements **JWT authentication, role-based authorization, project and task management, filtering, search, ordering, pagination, automated testing, PostgreSQL, Docker, and Gunicorn**.

## 🚀 Key Features

* 🔐 JWT Authentication & Token Refresh
* 🚪 JWT Logout with Token Blacklisting
* 👥 Role-Based Authorization

  * Owner
  * Admin
  * Member
* 📁 Project Management
* 👤 Project Member Management
* ✅ Task Management & Assignment
* 🔎 Filtering, Search & Ordering
* 📄 Pagination
* 🧪 Automated Testing
* 📊 Test Coverage
* 🐘 PostgreSQL
* 🐳 Docker & Docker Compose
* ⚡ Gunicorn
* 📚 OpenAPI / Swagger Documentation

## 🛠️ Tech Stack

**Backend**

* Python
* Django
* Django REST Framework

**Authentication & Security**

* Simple JWT
* Role-based permissions
* JWT token blacklisting

**Database**

* PostgreSQL

**DevOps**

* Docker
* Docker Compose
* Gunicorn

**Documentation & Testing**

* drf-spectacular
* Django Test Framework
* Coverage

## 📖 API Documentation

Once the application is running:

**Swagger UI**

```text
http://localhost:8000/api/docs/
```

**ReDoc**

```text
http://localhost:8000/api/redoc/
```

**OpenAPI Schema**

```text
http://localhost:8000/api/schema/
```
