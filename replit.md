# Task Management System

## Overview

This is a backend API for a task management system built with FastAPI and SQLAlchemy. The system provides RESTful endpoints for creating, reading, updating, and deleting tasks. Each task has a title, description, status, and due date. The API includes data validation through Pydantic schemas and supports database operations through SQLAlchemy ORM.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **FastAPI**: Modern Python web framework chosen for its automatic API documentation, built-in validation, and async support
- **SQLAlchemy ORM**: Database abstraction layer providing object-relational mapping and database-agnostic operations
- **Pydantic**: Data validation and serialization using Python type hints

### Database Design
- **Single Entity Model**: Simple Task model with fields for id, title, description, status, and due_date
- **SQLite Default**: Uses SQLite for local development with environment variable support for production databases
- **Auto-migration**: Database tables are created automatically on application startup

### API Structure
- **RESTful Design**: Standard HTTP methods (GET, POST, PUT, DELETE) for task operations
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