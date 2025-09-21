# Alumni Platform API Documentation

## Overview

This Django REST API provides comprehensive backend services for the Alumni Management Platform, supporting user management, social features, crowdfunding, mentorship, and administrative functions.

## Base URL
```
http://localhost:8000/api/
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "password_confirm": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "alumni",
  "linkedin_profile": "https://linkedin.com/in/johndoe",
  "current_position": "Software Engineer",
  "company": "Tech Corp",
  "graduation_year": 2020,
  "department": "Computer Science",
  "interests": ["Technology", "AI", "Mentorship"]
}
```

#### Login User
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Get User Profile
```http
GET /api/auth/profile/
Authorization: Bearer <token>
```

#### Update User Profile
```http
PUT /api/auth/profile/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Updated bio",
  "location": "San Francisco, CA"
}
```

## User Management

### User Discovery
```http
GET /api/auth/users/?user_type=alumni&department=Computer Science&search=john
```

### User Search
```http
POST /api/auth/users/search/
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "software engineer",
  "user_type": "alumni",
  "department": "Computer Science",
  "graduation_year": 2020,
  "interests": ["Technology", "AI"]
}
```

### User Connections
```http
# Get connections
GET /api/auth/connections/

# Send connection request
POST /api/auth/connections/request/123/

# Respond to connection request
POST /api/auth/connections/456/respond/
Content-Type: application/json
{
  "action": "accept"  // or "reject"
}
```

## Posts & Social Features

### Posts
```http
# Get posts feed
GET /api/posts/?post_type=achievement&page=1

# Create post
POST /api/posts/create/
Authorization: Bearer <token>
Content-Type: application/json
{
  "content": "Just got promoted!",
  "post_type": "achievement",
  "visibility": "public"
}

# Get post details
GET /api/posts/123/

# Like post
POST /api/posts/123/like/

# Comment on post
POST /api/posts/123/comment/
Content-Type: application/json
{
  "content": "Congratulations!"
}

# Share post
POST /api/posts/123/share/
Content-Type: application/json
{
  "platform": "linkedin"
}

# Bookmark post
POST /api/posts/123/bookmark/
```

## Crowdfunding

### Projects
```http
# Get projects
GET /api/crowdfunding/projects/?category=technology&status=active

# Create project
POST /api/crowdfunding/projects/create/
Authorization: Bearer <token>
Content-Type: application/json
{
  "title": "AI Study Assistant",
  "description": "An AI tool for personalized learning",
  "category": "technology",
  "target_amount": "25000.00",
  "duration_days": 30
}

# Get project details
GET /api/crowdfunding/projects/123/

# Contribute to project
POST /api/crowdfunding/projects/123/contribute/
Content-Type: application/json
{
  "amount": "100.00",
  "contribution_type": "one_time",
  "is_anonymous": false
}

# Get contributions
GET /api/crowdfunding/contributions/
```

### Project Updates
```http
# Get project updates
GET /api/crowdfunding/projects/123/updates/

# Create project update
POST /api/crowdfunding/projects/123/updates/create/
Content-Type: application/json
{
  "title": "Major Milestone Reached!",
  "content": "We've reached 50% of our funding goal!",
  "is_public": true
}
```

## Mentorship

### Mentor Profiles
```http
# Get mentors
GET /api/mentorship/mentors/?expertise=technology&availability=available

# Create mentor profile
POST /api/mentorship/mentors/profile/
Authorization: Bearer <token>
Content-Type: application/json
{
  "bio": "Experienced software engineer",
  "expertise_areas": "Python, JavaScript, React",
  "years_of_experience": 5,
  "max_mentees": 3
}
```

### Mentorship Requests
```http
# Get mentorship requests
GET /api/mentorship/requests/

# Create mentorship request
POST /api/mentorship/requests/create/
Content-Type: application/json
{
  "mentor": 123,
  "subject": "Career Guidance in Tech",
  "message": "Looking for guidance on transitioning to tech",
  "goals": "Learn about software engineering career paths"
}

# Respond to request
POST /api/mentorship/requests/456/respond/
Content-Type: application/json
{
  "action": "accept",  // or "reject"
  "mentor_response": "Happy to help!"
}
```

### Mentorship Sessions
```http
# Get sessions
GET /api/mentorship/sessions/

# Create session
POST /api/mentorship/sessions/
Content-Type: application/json
{
  "mentorship": 123,
  "title": "Career Planning Session",
  "session_type": "video_call",
  "scheduled_at": "2024-01-15T14:00:00Z",
  "duration_minutes": 60
}

# Start session
POST /api/mentorship/sessions/456/start/

# End session
POST /api/mentorship/sessions/456/end/
Content-Type: application/json
{
  "mentor_notes": "Great discussion about career goals",
  "action_items": "Research React.js courses"
}
```

## Clubs & Communities

### Clubs
```http
# Get clubs
GET /api/clubs/?category=technology&visibility=public

# Create club
POST /api/clubs/create/
Authorization: Bearer <token>
Content-Type: application/json
{
  "name": "Tech Innovation Society",
  "description": "A community of tech enthusiasts",
  "category": "technology",
  "visibility": "public"
}

# Join club
POST /api/clubs/123/join/

# Leave club
POST /api/clubs/123/leave/
```

### Club Events
```http
# Get club events
GET /api/clubs/123/events/

# Create event
POST /api/clubs/123/events/create/
Content-Type: application/json
{
  "title": "Tech Meetup",
  "description": "Monthly tech discussion",
  "event_type": "meeting",
  "start_date": "2024-01-15T18:00:00Z",
  "end_date": "2024-01-15T20:00:00Z",
  "location_type": "virtual",
  "meeting_link": "https://meet.google.com/abc-def-ghi"
}

# Register for event
POST /api/clubs/events/456/register/
```

## Notifications

### Get Notifications
```http
GET /api/notifications/?is_read=false&page=1
```

### Mark Notification as Read
```http
POST /api/notifications/123/mark-read/
```

### Mark All Notifications as Read
```http
POST /api/notifications/mark-all-read/
```

### Update Notification Preferences
```http
PUT /api/notifications/preferences/
Content-Type: application/json
{
  "email_connection_requests": true,
  "push_mentorship_requests": true,
  "digest_frequency": "daily"
}
```

## Analytics

### User Analytics
```http
# Get user engagement metrics
GET /api/analytics/user-engagement/

# Get platform metrics
GET /api/analytics/platform-metrics/?start_date=2024-01-01&end_date=2024-01-31
```

### Reports
```http
# User report
GET /api/analytics/reports/users/?user_type=alumni&department=Computer Science

# Activity report
GET /api/analytics/reports/activity/?start_date=2024-01-01&end_date=2024-01-31

# Financial report
GET /api/analytics/reports/financial/?start_date=2024-01-01&end_date=2024-01-31
```

## WebSocket Endpoints

### Real-time Notifications
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/notifications/123/');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'notification') {
        // Handle new notification
        console.log('New notification:', data.notification);
    }
};
```

## Error Handling

The API returns standard HTTP status codes and JSON error responses:

```json
{
  "error": "Error message",
  "details": "Additional error details",
  "field_errors": {
    "field_name": ["Field-specific error message"]
  }
}
```

## Pagination

List endpoints support pagination:

```json
{
  "count": 100,
  "next": "http://api.example.com/items/?page=2",
  "previous": null,
  "results": [...]
}
```

## Filtering and Search

Most list endpoints support filtering and search:

- `?search=query` - Search across relevant fields
- `?ordering=field_name` - Order by field (prefix with `-` for descending)
- `?page=2` - Page number
- `?page_size=20` - Items per page

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- 1000 requests per hour for authenticated users
- 100 requests per hour for anonymous users

## Webhooks

The API supports webhooks for real-time updates:

### Stripe Payment Webhooks
```http
POST /api/webhooks/stripe/
Content-Type: application/json
X-Stripe-Signature: <signature>

{
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      "id": "pi_1234567890",
      "amount": 10000,
      "status": "succeeded"
    }
  }
}
```

## SDK Examples

### JavaScript/TypeScript
```javascript
// Using fetch
const response = await fetch('/api/posts/', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

// Using axios
import axios from 'axios';

const api = axios.create({
  baseURL: '/api/',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const posts = await api.get('/posts/');
```

### Python
```python
import requests

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.get('/api/posts/', headers=headers)
posts = response.json()
```

## Testing

### Run Tests
```bash
python manage.py test
```

### API Testing with Postman
Import the Postman collection from `docs/postman_collection.json`

### Load Testing
```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/load_test.py --host=http://localhost:8000
```

## Deployment

### Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in production
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables
See `env.example` for required environment variables.

## Support

For API support and questions:
- Email: api-support@alumni-platform.com
- Documentation: https://docs.alumni-platform.com
- GitHub Issues: https://github.com/alumni-platform/api/issues
