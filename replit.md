# Task Management System

## Overview

This is a full-stack task management system built with FastAPI and SQLAlchemy. The system provides both a web interface and RESTful API endpoints for creating, reading, updating, and deleting tasks. Key features include user authentication with secure password hashing, advanced search and filtering capabilities, progress tracking, and comprehensive testing. Each task has a title, description, status, and due date. The application includes data validation through Pydantic schemas, HTML templates using Jinja2, user authentication with JWT tokens, and supports database operations through SQLAlchemy ORM with PostgreSQL database integration.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **FastAPI**: Modern Python web framework chosen for its automatic API documentation, built-in validation, and async support
- **SQLAlchemy ORM**: Database abstraction layer providing object-relational mapping and database-agnostic operations
- **Pydantic**: Data validation and serialization using Python type hints
- **Jinja2**: Template engine for rendering HTML pages with dynamic content

### Frontend Framework
- **HTML Templates**: Server-rendered HTML pages using Jinja2 templating
- **Bootstrap CSS**: Responsive UI framework for styling and layout
- **Form-based Interaction**: Traditional web forms for task creation and editing without JavaScript
- **Authentication UI**: Login and registration forms with error handling and user feedback

### Authentication System
- **User Management**: Registration and login functionality with secure password hashing
- **JWT Tokens**: JSON Web Token-based authentication stored in HTTP-only cookies
- **Password Security**: Bcrypt hashing for secure password storage
- **Session Management**: Automatic login/logout with token expiration

### Database Design
- **Multi-Entity Model**: Task and User models with relationship mapping
- **PostgreSQL Database**: Uses PostgreSQL database with automatic table creation on application startup
- **Database Indexes**: Optimized queries with indexes on status, due_date, and username fields
- **Foreign Key Relationships**: Tasks can be associated with users for future user-specific features
- **Environment-based Configuration**: Database connection managed through DATABASE_URL environment variable

### API Structure
- **Dual Interface**: Both web interface and REST API endpoints available
- **HTML Routes**: Server-rendered pages at `/`, `/tasks/new`, `/tasks/{id}`, `/tasks/{id}/edit`, `/tasks/{id}/delete`
- **Authentication Routes**: `/register`, `/login`, `/logout` for user management
- **API Routes**: JSON endpoints at `/api/tasks` with full CRUD operations and search capabilities
- **Search & Filter**: Query parameters for searching tasks by title/description and filtering by status
- **Response Models**: Consistent API responses using Pydantic schemas
- **Error Handling**: HTTP status codes and exception handling for invalid requests
- **CORS Enabled**: Cross-origin resource sharing configured for frontend integration

### Data Flow Architecture
- **Repository Pattern**: CRUD operations separated into dedicated functions in crud.py
- **Dependency Injection**: Database sessions managed through FastAPI's dependency system
- **Schema Validation**: Input/output validation through Pydantic models

### Key Architectural Decisions
- **PostgreSQL Production Database**: Using PostgreSQL for better performance and scalability
- **Separation of Concerns**: Clear separation between models, schemas, CRUD operations, authentication, and API endpoints
- **Type Safety**: Comprehensive type hints throughout the codebase for better development experience
- **Security First**: Password hashing, JWT tokens, and HTTP-only cookies for secure authentication
- **Search Optimization**: Database indexes and efficient query patterns for search and filtering

### Advanced Features
- **Progress Tracking**: Visual progress bar showing task completion percentage
- **Search Functionality**: Full-text search across task titles and descriptions
- **Status Filtering**: Filter tasks by completion status (Pending, In Progress, Completed)
- **User Authentication**: Secure registration and login system
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Comprehensive Testing**: Unit tests covering API endpoints and web pages

## External Dependencies

### Core Dependencies
- **FastAPI**: Web framework for building the REST API
- **Uvicorn**: ASGI server for running the FastAPI application
- **SQLAlchemy**: ORM for database operations and model definitions
- **Pydantic**: Data validation and serialization library
- **Jinja2**: Template engine for HTML rendering
- **Passlib**: Password hashing library with bcrypt support
- **Python-JOSE**: JWT token handling for authentication
- **Pytest**: Testing framework for unit tests
- **HTTPX**: HTTP client for API testing

### Database
- **PostgreSQL**: Production-ready database with full SQL support
- **Environment-based Configuration**: Configured through DATABASE_URL environment variable
- **Database Indexes**: Performance optimizations for search and filtering operations

### Development Tools
- **FastAPI Automatic Documentation**: Built-in Swagger UI at `/docs` endpoint
- **CORS Middleware**: Enabled for cross-origin requests (frontend integration ready)
- **Comprehensive Testing**: Unit tests covering all major functionality
- **Development Server**: Auto-reload during development for faster iteration

### Future Integration Points
- User-specific task management (tasks filtered by owner)
- Email notifications for due dates
- Task categories and tags
- Team collaboration features
- Mobile app integration via REST API
- Advanced analytics and reporting