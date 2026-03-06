# MovieWatch — Movie Theater Booking App

A Django web application that allows users to browse movies, book seats, and view their booking history. Built with Django 4.2, Django REST Framework, and tested with unittest and Behave BDD.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Seeding the Database](#seeding-the-database)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)

---

## Project Structure

```
hw2/
├── manage.py
├── db.sqlite3
│
├── movie_theater_booking/        # Project configuration
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── bookings/                     # Main application
│   ├── models.py                 # Movie, Seat, Booking models
│   ├── views.py                  # UI and API views
│   ├── urls.py                   # App URL routing
│   ├── serializers.py            # DRF serializers for API
│   ├── forms.py                  # Django forms
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py                  # Unit and integration tests
│   │
│   ├── templates/bookings/       # HTML templates
│   │   ├── movie_list.html       # Home page — lists all movies
│   │   ├── seat_booking.html     # Seat selection page
│   │   ├── booking_history.html  # User's booking history
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── static/css/               # Stylesheets
│   │   ├── base.css
│   │   └── seats.css
│   │
│   └── management/commands/
│       └── seed.py               # Custom management command to seed data
│
├── fixtures/                     # Initial data
│   ├── movies.json               # 10 sample movies
│   ├── seats.json                # 15 seats per movie (150 total)
│   └── bookings.json             # Empty by default
│
└── features/                     # BDD tests (Behave)
    ├── environment.py
    ├── auth.feature
    ├── movies.feature
    ├── seats.feature
    ├── bookings.feature
    └── steps/
        ├── auth.py
        ├── movies.py
        ├── seats.py
        └── bookings.py
```

---

## Features

- Browse a list of available movies
- View seat availability for each movie (15 seats per movie across rows A, B, and C)
- Register and log in to book seats
- Book available seats and view booking history
- REST API for movies, seats, and bookings
- Seats are automatically created when a new movie is added

---

## Setup

### Prerequisites

- Python 3.10+
- pip

### 1. Create and activate a virtual environment

```bash
python3 -m venv hw2_venv
source hw2_venv/bin/activate
```

### 2. Install dependencies

```bash
pip install django==4.2.11 djangorestframework behave django-behave
```

### 3. Apply migrations

```bash
cd hw2
python manage.py migrate
```

---

## Running the Application

```bash
python manage.py runserver
```

Then visit `http://localhost:8000` in your browser.

---

## Seeding the Database

To load the sample movies and seats:

```bash
python manage.py loaddata fixtures/movies.json
python manage.py loaddata fixtures/seats.json
python manage.py loaddata fixtures/bookings.json
```

> **Note:** Loading `movies.json` triggers a signal that auto-creates seats. If you then load `seats.json` it will create duplicates. Use the seed management command to avoid this:

```bash
python manage.py seed
```

To create an admin user for the Django admin panel at `/admin/`:

```bash
python manage.py createsuperuser
```

---

## Running Tests

### Unit and Integration Tests

Runs all model tests, view tests, and API integration tests:

```bash
python manage.py test bookings
```

For verbose output showing each individual test:

```bash
python manage.py test bookings --verbosity=2
```

### BDD Tests (Behave)

```bash
python manage.py behave
```

To run a specific feature file:

```bash
python manage.py behave features/bookings.feature
```

---

## API Endpoints

The REST API is available at `/api/` and provides a browsable interface when visited in a browser.

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/movies/` | List all movies | No |
| POST | `/api/movies/` | Create a movie | No |
| GET | `/api/movies/<id>/` | Retrieve a movie | No |
| PUT | `/api/movies/<id>/` | Update a movie | No |
| DELETE | `/api/movies/<id>/` | Delete a movie | No |
| GET | `/api/seats/` | List all seats | No |
| GET | `/api/seats/?movie=<id>` | Filter seats by movie | No |
| GET | `/api/bookings/` | List current user's bookings | Yes |
| POST | `/api/bookings/` | Create a booking | Yes |

### Example API usage

List all movies:
```bash
curl http://localhost:8000/api/movies/
```

Filter seats by movie:
```bash
curl http://localhost:8000/api/seats/?movie=1
```

Create a booking (requires authentication):
```bash
curl -u username:password \
  -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"movie": 1, "seat": 3}'
```

---

## Data Models

### Movie
| Field | Type | Description |
|-------|------|-------------|
| title | CharField | Title of the movie |
| description | TextField | Movie description |
| release_date | DateField | Release date |
| duration | IntegerField | Duration in minutes |

### Seat
| Field | Type | Description |
|-------|------|-------------|
| movie | ForeignKey | The movie this seat belongs to |
| seat_number | CharField | Seat identifier e.g. A1, B3 |
| is_booked | BooleanField | Whether the seat is booked |

### Booking
| Field | Type | Description |
|-------|------|-------------|
| movie | ForeignKey | The movie being booked |
| seat | ForeignKey | The seat being booked |
| user | ForeignKey | The user who made the booking |
| booking_date | DateTimeField | When the booking was made |
