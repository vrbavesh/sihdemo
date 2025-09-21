# Alumni Management Platform - Django Backend

## Project Structure

This Django backend provides a comprehensive API for the Alumni Management Platform, supporting user management, social features, crowdfunding, mentorship, and administrative functions.

## Quick Start

1. **Setup Virtual Environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

4. **Run Development Server**
```bash
python manage.py runserver
```

## API Documentation

- **Base URL**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`
- **API Documentation**: `http://localhost:8000/api/docs/` (Swagger UI)

## Key Features

- **User Management**: Registration, authentication, profile management
- **Social Features**: Posts, comments, likes, bookmarks
- **Crowdfunding**: Project creation, funding, payment processing
- **Mentorship**: Mentor-mentee matching, scheduling, progress tracking
- **Clubs & Communities**: Group management, events, discussions
- **Admin Dashboard**: User management, analytics, approvals
- **Real-time Features**: WebSocket support for live updates

## Technology Stack

- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT + OAuth2
- **Caching**: Redis
- **File Storage**: AWS S3 / Local
- **Payment**: Stripe integration
- **Real-time**: Django Channels (WebSockets)
- **Documentation**: drf-spectacular (OpenAPI 3.0)
