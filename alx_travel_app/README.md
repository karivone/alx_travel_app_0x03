# ALX Travel App

A Django-based travel application with REST API, Swagger documentation, and Celery task processing.

## Features

- RESTful API using Django REST Framework
- API Documentation with Swagger
- MySQL Database Integration
- Asynchronous Task Processing with Celery and RabbitMQ
- CORS Support

## Prerequisites

- Python 3.8+
- MySQL Server
- RabbitMQ Server

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/alx_travel_app.git
   cd alx_travel_app
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # OR
   source venv/bin/activate      # On Linux/Mac
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following content:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_NAME=alx_travel_db
   DATABASE_USER=your_db_user
   DATABASE_PASSWORD=your_db_password
   DATABASE_HOST=localhost
   DATABASE_PORT=3306
   ```

5. Create the MySQL database:
   ```
   mysql -u root -p
   CREATE DATABASE alx_travel_db;
   exit;
   ```

6. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

## Running the Application

1. Start the Django development server:
   ```
   python manage.py runserver
   ```

2. Start Celery worker:
   ```
   celery -A alx_travel_app worker -l info
   ```

3. Access the application:
   - Admin interface: http://localhost:8000/admin/
   - API documentation: http://localhost:8000/swagger/
   - API endpoints: http://localhost:8000/api/

## Project Structure

- `alx_travel_app/` - Main project directory
  - `settings.py` - Project settings
  - `urls.py` - Main URL configuration
  - `celery.py` - Celery configuration
- `listings/` - App for managing travel listings
  - `models.py` - Database models
  - `views.py` - API views
  - `urls.py` - App URL configuration
  - `serializers.py` - REST framework serializers
