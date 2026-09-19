# TeamTask API

A project and task management REST API built with **Django REST Framework**, designed to demonstrate real-world backend development concepts such as JWT authentication, role-based authorization, relational data modeling, API filtering, automated testing, PostgreSQL, Docker, and API documentation.

TeamTask allows authenticated users to create and manage projects, manage project members, and create and assign tasks while enforcing role-based permissions.

---

## 📌 Project Overview

**TeamTask API** is a backend REST API for managing collaborative projects and tasks.

The project was built to practice and demonstrate how a modern backend application is structured beyond basic CRUD operations.

The API includes:

* User registration and authentication
* JWT access and refresh tokens
* JWT token blacklisting for logout
* Role-based authorization
* Project management
* Project member management
* Task management
* Task assignment
* Filtering
* Searching
* Ordering
* Pagination
* Validation
* Automated API testing
* Test coverage
* PostgreSQL database
* Docker and Docker Compose
* Gunicorn
* OpenAPI / Swagger documentation
* Environment-based configuration

The project is intentionally focused on backend functionality rather than providing a frontend application.

---

# 🚀 Features

## Authentication

TeamTask uses **JWT (JSON Web Token)** authentication.

Users can:

* Register an account
* Obtain an access token
* Obtain a refresh token
* Refresh an expired access token
* Access protected API endpoints
* Logout by blacklisting the refresh token

Authentication is handled using Django REST Framework and Simple JWT.

### Authentication Flow

```text
User
 │
 │ Register
 ▼
Account Created
 │
 │ Login
 ▼
JWT Access + Refresh Tokens
 │
 ├── Access Token ──────► Protected API Requests
 │
 └── Refresh Token ─────► Obtain New Access Token
                              │
                              ▼
                         New Access Token
```

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

---

# 🔐 Authorization

Authentication determines **who the user is**.

Authorization determines **what that user is allowed to do**.

TeamTask implements role-based access control for project members.

The main project roles are:

| Role       | Responsibilities                                     |
| ---------- | ---------------------------------------------------- |
| **Owner**  | Full control over the project                        |
| **Admin**  | Administrative project/member management permissions |
| **Member** | Access to permitted project and task operations      |

Permissions are enforced at the API level rather than relying only on frontend restrictions.

This means a user cannot simply modify a request and gain access to an operation they are not authorized to perform.

---

# 📁 Project Management

Authenticated users can manage projects.

Project functionality includes:

* Creating projects
* Viewing projects
* Updating projects
* Deleting projects
* Viewing project-specific information
* Managing project members

Projects provide the organizational layer for tasks.

Conceptually:

```text
User
 │
 └── Project
      │
      ├── Members
      │
      └── Tasks
           │
           ├── Task 1
           ├── Task 2
           └── Task 3
```

---

# 👥 Project Members

Projects can contain multiple members.

Member management includes functionality for:

* Adding members
* Viewing project members
* Updating member information/role where permitted
* Removing members
* Applying role-based permissions

A user's ability to manage members depends on their role within the project.

This provides a basic team collaboration model similar to what is commonly required in project-management systems.

---

# ✅ Task Management

Tasks are associated with projects.

Task functionality includes:

* Creating tasks
* Viewing tasks
* Updating tasks
* Partially updating tasks
* Deleting tasks
* Assigning tasks
* Viewing tasks belonging to a specific project

Tasks are protected by authentication and project-level authorization.

---

# 🔎 Filtering

The API supports filtering to retrieve specific records based on supported fields.

Filtering allows clients to narrow down large collections instead of retrieving every record.

Example:

```http
GET /api/tasks/?status=completed
```

Filtering is implemented using Django Filter Backend.

---

# 🔍 Search

Search functionality allows users to search supported API resources using text-based queries.

Example:

```http
GET /api/tasks/?search=backend
```

Search functionality is implemented using Django REST Framework's search filtering support.

---

# ↕️ Ordering

The API supports ordering returned records.

Example:

```http
GET /api/tasks/?ordering=created_at
```

Descending ordering can be requested using:

```http
GET /api/tasks/?ordering=-created_at
```

This allows API clients to control how returned resources are ordered.

---

# 📄 Pagination

Collection endpoints support pagination so that large numbers of resources do not need to be returned in a single response.

Instead of:

```text
1000 tasks → one response
```

the API can return:

```text
Page 1 → limited number of tasks
Page 2 → next set of tasks
Page 3 → next set of tasks
```

Pagination improves API usability when working with larger datasets.

---

# ✔️ Validation

The API performs validation before creating or modifying resources.

Validation is handled primarily through Django REST Framework serializers.

This helps prevent invalid data from being stored in the database.

Examples of validation concerns include:

* Required fields
* Valid field formats
* Resource relationships
* Project/member relationships
* Task/project relationships
* Permission-related restrictions

---

# ⚠️ Error Handling

The API uses appropriate HTTP status codes and DRF responses to communicate the result of requests.

Common responses include:

| Status             | Meaning                              |
| ------------------ | ------------------------------------ |
| `200 OK`           | Request completed successfully       |
| `201 Created`      | Resource created successfully        |
| `204 No Content`   | Resource deleted successfully        |
| `400 Bad Request`  | Invalid request/data                 |
| `401 Unauthorized` | Authentication required or invalid   |
| `403 Forbidden`    | User authenticated but not permitted |
| `404 Not Found`    | Resource does not exist              |

This makes the API easier to consume from frontend applications, mobile applications, or other services.

---

# 🧪 Automated Testing

TeamTask includes automated tests for the API.

Testing covers important backend functionality including:

* Authentication
* Permissions
* Projects
* Project members
* Tasks
* Validation
* API behavior
* Authorization scenarios

The test suite currently contains:

```text
77 tests
```

The test suite has been executed successfully with:

```text
Found 77 test(s).
OK
```

Testing was performed using Django's testing framework / Django REST Framework's API testing tools.

---

# 📊 Test Coverage

Code coverage was also used to identify which parts of the project are exercised by the automated tests.

Coverage analysis helps identify:

* Tested code
* Untested code
* Missing test cases
* Areas that may require additional testing

The goal was not simply to write tests, but to use coverage information to identify gaps in the test suite.

---

# 🗄️ Database

TeamTask uses **PostgreSQL** as its relational database.

The project contains relationships between:

```text
Users
  │
  ├── Projects
  │      │
  │      ├── Members
  │      │
  │      └── Tasks
  │
  └── Tasks / Assignments
```

Using PostgreSQL allows the project to work with a production-style relational database instead of relying on SQLite during development.

---

# 🐳 Docker

The application can be run using Docker.

The Docker setup contains separate services for:

```text
┌─────────────────────┐
│      TeamTask       │
│      Django API     │
│      Gunicorn       │
└──────────┬──────────┘
           │
           │
┌──────────▼──────────┐
│     PostgreSQL      │
│      Database       │
└─────────────────────┘
```

Docker Compose is used to manage the application and database services.

This makes the development environment more consistent and reduces the amount of manual environment configuration required.

---

# 🏗️ Application Architecture

The project follows Django's application structure and separates functionality into multiple applications.

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
├── backend/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── manage.py
└── requirements.txt
```

### Application Responsibilities

### `accounts`

Responsible for:

* User accounts
* Registration
* Authentication-related functionality
* User profile functionality
* Account permissions

### `project`

Responsible for:

* Project management
* Project members
* Project-level authorization

### `tasks`

Responsible for:

* Task management
* Task assignment
* Task filtering
* Pagination
* Task-level authorization

### `backend`

Contains the main Django project configuration:

* Settings
* URL configuration
* WSGI
* ASGI

---

# 🔑 API Authentication Endpoints

The authentication system is based on JWT.

Typical authentication flow:

### Register

```http
POST /api/accounts/register/
```

Creates a new user account.

### Login

```http
POST /api/token/
```

Returns:

```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

### Refresh Access Token

```http
POST /api/token/refresh/
```

The refresh token is used to obtain a new access token without requiring the user to log in again.

### Logout

The refresh token can be blacklisted during logout so that it can no longer be used.

---

# 👤 User Profile

Authenticated users can access their own profile information.

Example:

```http
GET /api/accounts/me/
```

The endpoint requires authentication.

---

# 📚 API Endpoint Overview

The API is organized around three main areas:

```text
Authentication
    │
    ├── Registration
    ├── Login
    ├── Token Refresh
    └── Logout

Projects
    │
    ├── Project CRUD
    └── Project Members

Tasks
    │
    ├── Task CRUD
    ├── Task Assignment
    └── Project-specific Tasks
```

The exact endpoint definitions and request/response schemas are available through the generated OpenAPI documentation.

---

# 📖 API Documentation

TeamTask uses **drf-spectacular** to generate an OpenAPI schema and Swagger documentation.

After starting the application, the API documentation can be accessed through the configured Swagger/OpenAPI endpoints.

Swagger provides an interactive interface where API consumers can:

* Explore available endpoints
* Inspect request parameters
* View response schemas
* Understand authentication requirements
* Test API requests

This is particularly useful when integrating the backend with a frontend or another service.

---

# ⚙️ Environment Variables

Sensitive configuration values are stored outside the source code using environment variables.

Example environment configuration:

```env
SECRET_KEY=your-secret-key

DEBUG=False

DB_NAME=teamtask
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
```

The actual `.env` file is not committed to GitHub.

A `.env.example` file can be used as a template for local configuration.

> Never commit production secrets, database passwords, API keys, or JWT secrets to a public repository.

---

# 💻 Running the Project with Docker

## 1. Clone the repository

```bash
git clone https://github.com/aneeshbabug/TeamTask-API.git
```

Move into the project directory:

```bash
cd TeamTask-API
```

---

## 2. Create the environment file

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=teamtask
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
```

Use your own secure values.

---

## 3. Build the Docker containers

```bash
docker compose build
```

---

## 4. Start the application

```bash
docker compose up
```

The Django API will be available at:

```text
http://127.0.0.1:8000/
```

---

## 5. Run migrations

If migrations have not already been applied:

```bash
docker compose exec web python manage.py migrate
```

---

## 6. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

---

# 🐍 Running Without Docker

Docker is the recommended development setup for this project, but the Django application can also be run directly in a Python virtual environment.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables.

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will then be available at:

```text
http://127.0.0.1:8000/
```

---

# 🧪 Running Tests

To run the complete test suite:

```bash
docker compose exec web python manage.py test
```

The project test suite currently contains **77 tests**.

A successful run should look similar to:

```text
Found 77 test(s).
...
OK
```

---

# 📊 Running Coverage

If coverage is installed in the environment, coverage can be used to measure tested code.

Example:

```bash
coverage run manage.py test
```

Then generate the report:

```bash
coverage report
```

For an HTML report:

```bash
coverage html
```

The generated report can then be inspected to identify untested areas.

---

# 🔒 Security Considerations

TeamTask includes several security-oriented backend practices:

* JWT-based authentication
* Role-based authorization
* Protected API endpoints
* Password handling through Django-compatible hashing
* Environment-based secret configuration
* PostgreSQL instead of an embedded production database
* JWT refresh-token blacklisting for logout
* Permission checks at the API level
* `.env` excluded from version control

The project is intended as a portfolio/learning backend and is not presented as a fully deployed production service.

For a real production deployment, additional infrastructure and security configuration would be required, including HTTPS, secure cookie configuration where applicable, production environment settings, monitoring, deployment infrastructure, and other operational controls.

---

# 🧩 Technologies Used

| Technology                                    | Purpose                            |
| --------------------------------------------- | ---------------------------------- |
| **Python**                                    | Backend programming language       |
| **Django**                                    | Web framework                      |
| **Django REST Framework**                     | REST API development               |
| **Simple JWT**                                | JWT authentication                 |
| **PostgreSQL**                                | Relational database                |
| **django-filter**                             | API filtering                      |
| **drf-spectacular**                           | OpenAPI / Swagger documentation    |
| **Gunicorn**                                  | WSGI application server            |
| **Docker**                                    | Containerization                   |
| **Docker Compose**                            | Multi-container development        |
| **Git / GitHub**                              | Version control and source hosting |
| **Django Test Framework / DRF testing tools** | Automated testing                  |
| **Coverage.py**                               | Test coverage analysis             |

---

# 🧠 Backend Concepts Demonstrated

This project was built to demonstrate practical understanding of backend development concepts including:

### API Development

* REST architecture
* HTTP methods
* HTTP status codes
* Request/response handling
* Serializers
* API validation

### Authentication

* User registration
* JWT access tokens
* JWT refresh tokens
* Token expiration
* Token blacklisting
* Protected endpoints

### Authorization

* Role-based permissions
* Object-level access control
* Project membership
* Permission enforcement

### Database

* Relational data modeling
* Foreign-key relationships
* PostgreSQL
* Django ORM
* Migrations

### API Features

* Filtering
* Searching
* Ordering
* Pagination

### Software Quality

* Automated testing
* Test coverage
* API documentation
* Environment-based configuration

### Deployment-Oriented Development

* Docker
* Docker Compose
* Gunicorn
* Containerized PostgreSQL

---

# 🔄 Example Request Flow

A typical authenticated request follows this flow:

```text
Client
  │
  │ POST /api/token/
  ▼
Authentication
  │
  │ Access + Refresh Token
  ▼
Client
  │
  │ Authorization: Bearer <access_token>
  ▼
Django REST Framework
  │
  ├── Authentication
  │
  ├── Permission Check
  │
  ├── Serializer Validation
  │
  ├── Business Logic
  │
  └── Database Operation
  │
  ▼
JSON Response
```

This demonstrates the basic lifecycle of an authenticated API request.

---

# 📌 Example Use Case

A typical TeamTask workflow could look like:

```text
1. User registers
        ↓
2. User logs in
        ↓
3. JWT tokens are issued
        ↓
4. User creates a project
        ↓
5. User adds project members
        ↓
6. Members receive appropriate roles
        ↓
7. Tasks are created
        ↓
8. Tasks are assigned to members
        ↓
9. Members retrieve/filter/search tasks
        ↓
10. Role permissions control available operations
```

---

# 🗂️ Project Status

**Status: Completed portfolio project**

The current version focuses on demonstrating the core backend functionality and engineering practices implemented during development.

The project is available publicly on GitHub:

**Repository:**
https://github.com/aneeshbabug/TeamTask-API

---

# 🔮 Future Improvements

Possible future improvements include:

* Production deployment
* HTTPS configuration
* CI/CD pipeline
* API rate limiting
* Advanced monitoring and logging
* Email-based account verification
* Password reset functionality
* More comprehensive API documentation
* Additional automated tests
* Performance optimization
* Database indexing where appropriate
* Background task processing
* Notifications
* Real-time updates using WebSockets
* Frontend client
* Advanced project analytics

These are intentionally outside the scope of the current version.

---

# 🎯 What I Learned

Building TeamTask helped me move beyond basic Django CRUD applications and understand how different backend components work together.

Key areas I practiced include:

* Designing REST APIs
* Building authentication systems
* Implementing JWT authentication
* Designing authorization rules
* Working with relational databases
* Building reusable serializers and views
* Writing automated tests
* Measuring test coverage
* Documenting APIs
* Containerizing applications
* Using PostgreSQL with Django
* Running Django with Gunicorn
* Managing secrets through environment variables
* Structuring a multi-application Django project

---

# 👨‍💻 Author

**Aneesh Babu G**

GitHub:
https://github.com/aneeshbabug

---

## ⭐ Project

If you find the project useful or interesting, feel free to explore the repository and the implementation.

**TeamTask API — Django REST Framework project and task management backend.**
