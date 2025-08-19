# Task Management System

## Overview

This is a full-stack task management system built with FastAPI and SQLAlchemy. The system provides both a web interface and RESTful API endpoints for creating, reading, updating, and deleting tasks. Each task has a title, description, status, and due date. The application includes data validation through Pydantic schemas, HTML templates using Jinja2, and supports database operations through SQLAlchemy ORM with PostgreSQL database integration.

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

### Database Design
- **Single Entity Model**: Simple Task model with fields for id, title, description, status, and due_date
- **PostgreSQL Database**: Uses PostgreSQL database with automatic table creation on application startup
- **Environment-based Configuration**: Database connection managed through DATABASE_URL environment variable

### API Structure
- **Dual Interface**: Both web interface and REST API endpoints available
- **HTML Routes**: Server-rendered pages at `/`, `/tasks/new`, `/tasks/{id}`, `/tasks/{id}/edit`, `/tasks/{id}/delete`
- **API Routes**: JSON endpoints at `/api/tasks` with full CRUD operations
- **Response Models**: Consistent API responses using Pydantic schemas
- **Error Handling**: HTTP status codes and exception handling for invalid requests
- **CORS Enabled**: Cross-origin resource sharing configured for frontend integration

### Data Flow Architecture
- **Repository Pattern**: CRUD operations separated into dedicated functions in crud.py
- **Dependency Injection**: Database sessions managed through FastAPI's dependency system
- **Schema Validation**: Input/output validation through Pydantic models

### Key Architectural Decisions
- **SQLite to Production Database**: Flexible database configuration allowing easy migration from SQLite to PostgreSQL/MySQL
- **Separation of Concerns**: Clear separation between models, schemas, CRUD operations, and API endpoints
- **Type Safety**: Comprehensive type hints throughout the codebase for better development experience

## External Dependencies

### Core Dependencies
- **FastAPI**: Web framework for building the REST API
- **Uvicorn**: ASGI server for running the FastAPI application
- **SQLAlchemy**: ORM for database operations and model definitions
- **Pydantic**: Data validation and serialization library

### Database
- **SQLite**: Default local database (development)
- **Environment-based Configuration**: Support for PostgreSQL, MySQL, or other databases through DATABASE_URL environment variable

### Development Tools
- **FastAPI Automatic Documentation**: Built-in Swagger UI at `/docs` endpoint
- **CORS Middleware**: Enabled for cross-origin requests (frontend integration ready)

### Future Integration Points
- Database migration to PostgreSQL or MySQL for production
- Authentication and authorization system
- Frontend application integration
- Task filtering and search capabilities