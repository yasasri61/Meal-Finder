# MealFinder — Full Stack Python

A portfolio-ready meal discovery web application built with Django, Django REST Framework, SQLite, HTML/CSS, Bootstrap, and vanilla JavaScript.

## Features

- Responsive modern UI/UX
- User registration, login and logout
- Meal search
- Category and cuisine filters
- Cooking-time filter
- Ingredient-based meal finder with match scores
- Meal details with ingredients and instructions
- Favorites
- Ratings and reviews
- Recently viewed meals
- User profile
- Django admin for meal/category management
- JSON REST API
- Pagination
- Form validation and friendly error states
- SQLite database for easy local setup

## Tech Stack

- Python 3.10+
- Django 5
- Django REST Framework
- SQLite
- Bootstrap 5
- Vanilla JavaScript
- HTML5/CSS3

## Project Structure

```text
meal-finder/
├── manage.py
├── requirements.txt
├── README.md
├── config/
├── accounts/
├── meals/
├── favorites/
├── reviews/
├── templates/
└── static/
```

## Run on Windows

```powershell
cd meal-finder
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## Run on macOS/Linux

```bash
cd meal-finder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Demo account

The seed command creates:

- Email: `demo@mealfinder.local`
- Password: `Demo@12345`

Change this password before using the project publicly.

## REST API

- `GET /api/meals/`
- `GET /api/meals/?search=chicken`
- `GET /api/meals/?category=Vegetarian`
- `GET /api/meals/?cuisine=Indian`
- `GET /api/meals/?max_time=30`
- `GET /api/meals/<id>/`
- `GET /api/categories/`

The API returns JSON and can be tested from a browser, Postman, or JavaScript.

## Notes

Meal images in the seed data use remote Unsplash URLs. The application still works without them and displays a styled fallback when an image is unavailable.

For production, set these environment variables before deployment:

```text
DEBUG=False
DJANGO_SECRET_KEY=<a-long-random-secret>
ALLOWED_HOSTS=your-domain.example
```

Vercel supplies `VERCEL_URL` automatically. The project also allows the current Vercel domain, `mealfinder-olive.vercel.app`, by default. For production, use PostgreSQL, configure static/media storage, and use HTTPS.
