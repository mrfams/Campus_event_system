# Campus Event System

A Django-based platform for managing campus events and clubs.

## Overview

## Project Setup

### Requirements
- Python 3.8+
- Django 4.0+
- Pillow (for image uploads)


### Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Migrations
If you make changes to models, generate and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Media Files
- `MEDIA_URL = /media/`
- `MEDIA_ROOT = media/`
- Profile pictures uploaded to `media/profiles/`
- Club logos uploaded to `media/club_logos/`

## User Roles

### Student
- Join/leave clubs
- Register for events
- View approved clubs and events
- Comment on events

### Club Manager
- Create and manage own clubs
- Create and manage own events
- View dashboard with club statistics

### Admin
- Approve/reject clubs
- View all clubs and events
- Manage users (change roles, block/unblock, delete)
- View admin dashboard with statistics

## Features

### User Management
- Registration and login
- Profile editing with profile picture upload
- Role-based access control
- User blocking functionality (admin only)

### Club Management
- Club creation (club managers and admins)
- Club approval (admin only)
- Club rejection (admin only)
- Club deletion (admin and club manager)
- Club categories for organization
- Club logo upload

### Event Management
- Event creation within clubs
- Event registration with capacity validation
- Duplicate registration prevention
- Event comments
- Event deletion (admin and club manager)
- Event search and filtering by category
- Participant list visible to club managers

### Admin Features
- Dashboard with statistics
- Club approval queue
- User management
- Event management

### API Endpoints (Django REST Framework)
- `/api/users/` - User list
- `/api/clubs/` - Approved clubs
- `/api/club-categories/` - Club categories
- `/api/events/` - Approved events
- `/api/event-comments/` - Event comments

## Validation Rules

### Event Registration
- Prevents duplicate registration
- Stops registration when event is full (`participants >= max_participants`)

## Templates

- `templates/home.html` - Home page with featured clubs and events
- `templates/users/login.html` - Login page
- `templates/users/register.html` - Registration page
- `templates/users/profile.html` - User profile
- `templates/users/profile_edit.html` - Profile editing
- `templates/clubs/club_list.html` - Club listing
- `templates/clubs/club_detail.html` - Club details
- `templates/clubs/manager_dashboard.html` - Club manager dashboard
- `templates/clubs/club_form.html` - Club creation/edit
- `templates/events/event_list.html` - Event listing with search/filter
- `templates/events/event_detail.html` - Event details
- `templates/events/event_form.html` - Event creation/edit
- `templates/users/admin/` - Admin templates

## URLs

- `/` - Home
- `/login/` - Login
- `/register/` - Register
- `/profile/` - Profile
- `/profile/edit/` - Edit profile
- `/clubs/` - Club list
- `/clubs/<pk>/` - Club detail
- `/clubs/create/` - Create club
- `/clubs/dashboard/` - Club manager dashboard
- `/events/` - Event list
- `/events/<pk>/` - Event detail
- `/events/<pk>/participants/` - Event participants list
- `/admin/` - Admin dashboard
- `/admin/users/` - User management
- `/admin/clubs/` - Club approval