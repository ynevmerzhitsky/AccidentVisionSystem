# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Install system dependencies for PostgreSQL and RabbitMQ (if needed)
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Ensure that .env is loaded in Django and Celery
# For reading .env in settings.py
RUN pip install python-dotenv

# Default command (can be overridden by docker-compose)
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]
