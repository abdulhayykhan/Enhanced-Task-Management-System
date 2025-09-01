# ✅ Enhanced Task Management System  

[![View App Live](https://img.shields.io/badge/🚀%20View%20App-Live-green?style=for-the-badge)](https://enhanced-task-management-system.onrender.com/login)      [![View on LinkedIn](https://img.shields.io/badge/💼%20View%20Post-LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/abdul-hayy-khan/)  

---

## 📌 Overview  

The **Enhanced Task Management System** is a **full-stack collaborative web app** built with **FastAPI** and **SQLAlchemy**, featuring both a **web interface** and **RESTful APIs**.  

It enables users to:  
✔️ Register & login securely with email authentication  
✔️ Create, update, delete, and share tasks  
✔️ Get **real-time notifications** via WebSockets  
✔️ Search & filter tasks dynamically  
✔️ Track task progress with visual indicators  

🔹 Each task includes a **title, description, due date, and status**.  
🔹 Collaboration is enabled through **email-based task sharing**, with dedicated views for:  
- **Tasks Shared with Me**  
- **Tasks I’ve Shared**  

---

## ⚙️ System Architecture  

### 🔹 Backend  
- **FastAPI** – High-performance Python web framework (async-ready)  
- **SQLAlchemy ORM** – Database models & queries  
- **Pydantic** – Data validation & serialization  
- **Jinja2** – HTML templating  

### 🔹 Frontend  
- **Bootstrap 5 + Custom CSS** – Responsive, mobile-friendly UI  
- **Server-side templates (Jinja2)** – Dynamic HTML rendering  
- **Form-based interaction** – No external JS frameworks  

### 🔹 Authentication  
- Email-based registration/login (with full name)  
- **JWT tokens** stored in HTTP-only cookies  
- **Bcrypt password hashing** for security  
- Automatic session expiration  
- User identity shown throughout the interface  

### 🔹 Database  
- **PostgreSQL (production)** + **SQLite (development)**  
- Entities: **User, Task, Notification**  
- **Many-to-many** task sharing via `task_shares` table  
- **Indexes** on status, due_date, email for fast queries  
- Persistent notification storage with **read/unread tracking**  

### 🔹 API & Routes  
- **RESTful API Endpoints** (`/api/tasks`)  
- Web routes for CRUD & authentication (`/register`, `/login`, `/tasks/new`)  
- **Collaboration routes** (`/tasks/shared`, `/tasks/{id}/share`)  
- **WebSocket endpoint** (`/ws/{user_id}`) for real-time notifications  
- Built-in **Swagger UI** at `/docs`  

---

## 🌟 Features  

- 👤 **User Authentication** (JWT + bcrypt)  
- 📝 **Task CRUD operations** (title, description, due date, status)  
- 📤 **Task sharing via email** with permission-based access  
- 🔔 **Real-time notifications** using WebSockets  
- 📊 **Progress bar** for task completion  
- 🔎 **Advanced search & filtering** (status, text search)  
- 📱 **Responsive UI** (Bootstrap)  
- 🧪 **Unit testing** with Pytest & HTTPX  
- 🛡 **Data validation** with Pydantic  

---

## 🏗 Key Decisions  

- **PostgreSQL** for scalability & reliability  
- **Separation of concerns**: models, schemas, CRUD, routes, auth  
- **Security-first**: password hashing, JWT tokens, HTTP-only cookies  
- **Type safety** with Python hints  
- **Repository pattern** for clean data access  
- **Optimized DB queries** with indexes  

---

## 🤝 Collaboration Features  

- Share tasks with other users via **email**  
- Separate dashboards:  
  - **Tasks Shared with Me**  
  - **Tasks I’ve Shared**  
- **Permission-based access**: owners edit, recipients view-only  
- **Real-time status change alerts**  
- **Persistent notifications** (stored + delivered live)  

---

## 🧪 Testing & Validation  

- **Pytest** for unit & integration tests  
- **Pydantic schemas** for request/response validation  
- **HTTPX client** for API testing  
- Coverage: authentication, CRUD, sharing, notifications  

---

## 📦 Dependencies  

**Core:** FastAPI, SQLAlchemy, Pydantic, Jinja2, Uvicorn  
**Security:** Passlib (bcrypt), Python-JOSE (JWT)  
**Realtime:** WebSockets  
**Testing:** Pytest, HTTPX  
**Database:** PostgreSQL (prod), SQLite (local dev)  

---

## 🔮 Future Roadmap  

- 📧 Email reminders for due dates  
- 🏷 Task categories & tags  
- 📊 Analytics & reporting  
- 👥 Team workspaces & projects  
- 📱 Mobile app integration (via REST API)  
- 📎 File attachments  
- 💬 Task comments/discussions  

---

## 📂 Project Structure  

```
Enhanced-Task-Management-System/
├── main.py # Entry point
├── auth.py # Authentication (JWT, login, register)
├── crud.py # CRUD operations
├── database.py # DB connection
├── models.py # SQLAlchemy models
├── notifications.py # WebSocket notifications
├── schemas.py # Pydantic schemas
├── static/ # CSS, JS, images
├── templates/ # Jinja2 HTML templates
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── tasks.html
│ ├── shared_tasks.html
│ └── analytics.html
├── tests/ # Pytest test cases
│ ├── test_main.py
│ └── test_comprehensive.py
├── requirements.txt # Dependencies
└── README.md # Documentation
```

---

## 🚀 Running Locally
```
# Clone repo
git clone https://github.com/abdulhayykhan/Enhanced-Task-Management-System.git
cd Enhanced-Task-Management-System

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # On Windows
source .venv/bin/activate     # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run FastAPI app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Open http://127.0.0.1:8000/login to get started
# API docs at http://127.0.0.1:8000/docs
```

---

## 🙋‍♂️ Author

**Abdul Hayy Khan**

📫 abdulhayykhan.1@gmail.com

---

## 📌 License

This project is for educational purposes as part of the **DeveloperHub Corporation** internship program. Feel free to use it for learning and inspiration. Attribution is appreciated.

---
