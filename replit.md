# Task Management System

## Overview

This is a full-stack collaborative task management system built with FastAPI and SQLAlchemy. The system provides both a web interface and RESTful API endpoints for creating, reading, updating, and deleting tasks. Key features include email-based user authentication with full name registration, task sharing via email addresses, real-time notifications via WebSockets, advanced search and filtering capabilities, progress tracking, and comprehensive testing. Each task has a title, description, status, due date, and can be shared with multiple users via their email addresses. The application includes data validation through Pydantic schemas, HTML templates using Jinja2, JWT token authentication, real-time collaboration features, and supports database operations through SQLAlchemy ORM with PostgreSQL database integration. The system now features dedicated shared task views separating "Tasks Shared with Me" and "Tasks I've Shared" for better collaboration management.

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
- **Email-based Registration**: Users register with full name, email address, and password
- **Email Login**: Authentication using email address instead of username
- **JWT Tokens**: JSON Web Token-based authentication stored in HTTP-only cookies
- **Password Security**: Bcrypt hashing for secure password storage
- **Session Management**: Automatic login/logout with token expiration
- **User Identity**: Full name and email displayed throughout the interface

### Database Design
- **Multi-Entity Model**: Task, User, and Notification models with complex relationship mapping
- **Updated User Model**: Users have name and email fields instead of username
- **Task Sharing**: Many-to-many relationship between tasks and users via task_shares association table
- **PostgreSQL Database**: Uses PostgreSQL database with automatic table creation on application startup
- **Database Indexes**: Optimized queries with indexes on status, due_date, email, and notification fields
- **Foreign Key Relationships**: Tasks have owners and can be shared with multiple users
- **Notification System**: Persistent notification storage with read/unread status tracking
- **Environment-based Configuration**: Database connection managed through DATABASE_URL environment variable

### API Structure
- **Dual Interface**: Both web interface and REST API endpoints available
- **HTML Routes**: Server-rendered pages at `/`, `/tasks/new`, `/tasks/{id}`, `/tasks/{id}/edit`, `/tasks/{id}/delete`
- **Authentication Routes**: `/register`, `/login`, `/logout` for user management
- **Collaboration Routes**: `/tasks/{id}/share`, `/tasks/shared`, `/notifications` for team features
- **WebSocket Endpoint**: `/ws/{user_id}` for real-time notification delivery
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
- **Task Collaboration**: Share tasks with other users for collaborative work
- **Real-time Notifications**: WebSocket-powered instant notifications for task updates
- **Notification Management**: Persistent notification system with read/unread tracking
- **Task Ownership**: Clear distinction between task owners and shared users
- **Status Change Alerts**: Automatic notifications when shared task status changes
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Comprehensive Testing**: Unit tests covering API endpoints and web pages

### Collaboration Features
- **Email-based Task Sharing**: Task owners can share tasks by entering recipient email addresses
- **Dual Shared Task Views**: Separate views for "Tasks Shared with Me" and "Tasks I've Shared"
- **Real-time Updates**: WebSocket connections for instant notifications
- **Notification System**: Database-persisted notifications with WebSocket delivery
- **User Collaboration**: Multiple users can view shared tasks with appropriate permissions
- **Status Notifications**: Automatic alerts when shared tasks are updated
- **Permission-based Access**: Shared tasks are view-only for recipients, full control for owners
- **Email Validation**: System validates email addresses exist before allowing task sharing

## External Dependencies

### Core Dependencies
- **FastAPI**: Web framework for building the REST API with WebSocket support
- **Uvicorn**: ASGI server for running the FastAPI application
- **SQLAlchemy**: ORM for database operations and model definitions
- **Pydantic**: Data validation and serialization library
- **Jinja2**: Template engine for HTML rendering
- **Passlib**: Password hashing library with bcrypt support
- **Python-JOSE**: JWT token handling for authentication
- **WebSockets**: Real-time communication for instant notifications
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
- Email notifications for due dates and task updates
- Task categories and tags for better organization
- Advanced task filtering (by owner, shared status, date ranges)
- Team workspaces and project management
- Mobile app integration via REST API
- Advanced analytics and reporting
- File attachments to tasks
- Task comments and discussion threads