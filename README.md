# Enhanced Task Management System

[![View App Live](https://img.shields.io/badge/🚀%20View%20App-Live-green?style=for-the-badge)](https://enhanced-task-management-system.onrender.com/login)

## 📌 Overview
This is a full-stack collaborative task management system built with **FastAPI** and **SQLAlchemy**.  
The system provides both a web interface and RESTful API endpoints for creating, reading, updating, and deleting tasks.  

Key features include:
- Email-based user authentication with full name registration
- Task sharing via email addresses
- Real-time notifications via WebSockets
- Advanced search and filtering capabilities
- Progress tracking
- Comprehensive testing  

Each task has a title, description, status, due date, and can be shared with multiple users via their email addresses.  
The system now features dedicated shared task views separating **"Tasks Shared with Me"** and **"Tasks I've Shared"** for better collaboration management.

---

## ⚙️ System Architecture

### 🔹 Backend Framework
- **FastAPI** – Modern Python web framework with automatic API docs and async support  
- **SQLAlchemy ORM** – Database abstraction layer with ORM support  
- **Pydantic** – Data validation and serialization  
- **Jinja2** – Template engine for server-rendered HTML  

### 🔹 Frontend Framework
- **HTML Templates (Jinja2)** – Dynamic server-side rendering  
- **Bootstrap CSS** – Responsive UI & layout  
- **Form-based Interaction** – Traditional forms for CRUD operations  
- **Authentication UI** – Login & registration with feedback  

### 🔹 Authentication System
- **Email-based Registration** – Full name, email, password  
- **Email Login** – Login using email instead of username  
- **JWT Tokens** – Stored in HTTP-only cookies  
- **Password Security** – Bcrypt hashing  
- **Session Management** – Auto token expiration  
- **User Identity** – Name & email displayed in UI  

### 🔹 Database Design
- **Entities** – Task, User, Notification  
- **User Model** – Name + Email (unique)  
- **Task Sharing** – Many-to-many relation (`task_shares` table)  
- **PostgreSQL Database** – Production-ready with table auto-creation  
- **Indexes** – Optimized on status, due_date, email, notifications  
- **Relationships** – Tasks linked to owners and shared users  
- **Notification System** – Stored in DB with read/unread status  
- **Configurable DB** – `DATABASE_URL` environment variable  

### 🔹 API Structure
- **Dual Interface** – Web UI + REST API  
- **HTML Routes** – `/`, `/tasks/new`, `/tasks/{id}`, `/tasks/{id}/edit`, `/tasks/{id}/delete`  
- **Authentication Routes** – `/register`, `/login`, `/logout`  
- **Collaboration Routes** – `/tasks/{id}/share`, `/tasks/shared`, `/notifications`  
- **WebSocket Endpoint** – `/ws/{user_id}` for notifications  
- **API Routes** – `/api/tasks` with CRUD + search  
- **Search & Filter** – Query params for search and status  
- **Response Models** – Standardized with Pydantic  
- **Error Handling** – Proper HTTP codes  
- **CORS Enabled** – For future frontend integration  

### 🔹 Data Flow
- **Repository Pattern** – CRUD operations in `crud.py`  
- **Dependency Injection** – Session management via FastAPI  
- **Schema Validation** – Input/output via Pydantic  

---

## 🏗 Key Decisions
- PostgreSQL chosen for scalability  
- Separation of concerns (models, schemas, CRUD, auth, routes)  
- Strong typing with Python type hints  
- Security first (hashing, JWT, cookies)  
- Optimized search queries with DB indexes  

---

## 🌟 Advanced Features
- Progress bar showing task completion %  
- Full-text search in title & description  
- Status filtering (Pending, In Progress, Completed)  
- Secure registration & login  
- Email-based task collaboration  
- Real-time WebSocket notifications  
- Persistent notification history  
- Ownership vs shared access  
- Alerts on status change  
- Responsive Bootstrap design  
- Unit tests for API & web routes  

---

## 🤝 Collaboration Features
- Share tasks **via email**  
- Separate views: **Shared with Me** vs **I’ve Shared**  
- Real-time notifications for updates  
- Permission-based: owners control, recipients read-only  
- Email validation before sharing  

---

## 📦 External Dependencies

### Core
- **FastAPI**  
- **Uvicorn**  
- **SQLAlchemy**  
- **Pydantic**  
- **Jinja2**  
- **Passlib (bcrypt)**  
- **Python-JOSE (JWT)**  
- **WebSockets**  
- **Pytest**  
- **HTTPX**  

### Database
- **PostgreSQL** (via `DATABASE_URL`)  
- **Indexes** for fast queries  

### Dev Tools
- Built-in FastAPI docs (`/docs`)  
- CORS middleware  
- Unit tests with Pytest  
- Auto-reload dev server  

---

## 🔮 Future Improvements
- Email notifications for due dates  
- Task categories & tags  
- Advanced filters (owner, date range, etc.)  
- Team workspaces  
- Mobile app integration (REST API)  
- More analytics & reporting  
- File attachments  
- Task comments/discussions  

---

## 📁 Project Structure

Enhanced-Task-Management-System/
- ├── main.py                 - Entry point of the FastAPI application
- ├── auth.py                 - Authentication & authorization (JWT, login, register)
- ├── crud.py                 - CRUD operations (users, tasks, shares)
- ├── database.py             - Database connection and session management
- ├── models.py               - SQLAlchemy ORM models (User, Task, Notification, Shares)
- ├── notifications.py        - Real-time notifications (WebSockets, persistence)
- ├── schemas.py              - Pydantic schemas for validation & serialization
- ├── tasks.db                - SQLite database file (local development)
- ├── requirements.txt        - Python dependencies
- ├── test_comprehensive.py   - Comprehensive test cases for the app
- ├── test_main.py            - Unit tests for API and web routes
- ├── static/                 - Static assets (CSS, JS, images)
  - │   └── sw.js             - Service Worker for caching/notifications
- ├── templates/              - Jinja2 HTML templates
  - │   ├── base.html           - Base layout template
  - │   ├── login.html          - Login page
  - │   ├── register.html       - Registration page
  - │   ├── tasks.html          - Task list & dashboard
  - │   ├── task_detail.html    - Task detail view
  - │   ├── task_edit.html      - Edit task form
  - │   ├── task_new.html       - Create new task form
  - │   ├── shared_tasks.html   - Tasks shared with the user
  - │   └── analytics.html      - Analytics & progress tracking
- └── README.md              - Project documentation

---

## 🚀 Running Locally
```
# Clone repo
git clone https://github.com/your-username/task-management-system.git
cd task-management-system

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Open http://127.0.0.1:8000/login to get started
# API docs at http://127.0.0.1:8000/docs
```

---

## 📢 LinkedIn & GitHub Showcase

I’ll be posting a video and write-up on my [LinkedIn](https://www.linkedin.com/in/abdul-hayy-khan) profile showcasing this project and experience.

[![View on LinkedIn](https://img.shields.io/badge/💼%20View%20Post-LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/abdul-hayy-khan/)

---

## 🙋‍♂️ Author

**Abdul Hayy Khan**

📫 abdulhayykhan.1@gmail.com

---

## 📌 License

This project is for educational purposes as part of the **DeveloperHub Corporation** internship program. Feel free to use it for learning and inspiration. Attribution is appreciated.

---
