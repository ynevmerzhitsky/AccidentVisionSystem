# AccidentVisionSystem

## Overview of Infrastructure and Architecture

AccidentVisionSystem is a modular expert system for detecting road incidents in historical videos using Django, PostgreSQL, RabbitMQ, and Celery within Docker Compose.

## Components

* **Django Web Service**: Handles user authentication (registration, login, password recovery), file uploads, task submission, and displaying results. Uses `python-dotenv` to load environment variables from `.env`.
* **PostgreSQL Database**: Stores user accounts, video metadata, and analysis records. Configured in `settings.py` via Django's `DATABASES` setting.
* **RabbitMQ**: Serves as the message broker for Celery tasks; stores task messages and result queues.
* **Celery Worker**: Consumes tasks, processes video files from the shared `videos` volume, runs detection models, and writes analysis results back to RabbitMQ.


## Docker Compose

* **Shared Volume**: Named volume `videos` mounted into both `web` and `worker` containers for file exchange.
* **Docker Compose**: Defines and links all services (`web`, `worker`, `consumer`, `db`, `rabbitmq`), loads `.env`, and mounts volumes.

## Directory Structure

```text
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── accidentvision/          # Django project
│   ├── settings.py
│   ├── celery.py
│   └── ...
├── core/                    # Django app
│   ├── models.py
│   ├── tasks.py
│   ├── views.py
│   └── ...
├── videos/                  # Shared folder for videos
└── README.md
```

## Setup Options

Choose the workflow that works best for you:

- [App without Docker](#step-by-step-setup-instructions-app-without-docker)  
- [App in Docker](#step-by-step-setup-instructions-app-in-docker)

## Step-by-Step Setup Instructions (App in Docker)

### Prerequisites

* Docker >= 20.10
* Docker Compose >= 1.29
* Git
* Python >= 3.8

### 1. Clone the Repository

```bash
git clone https://github.com/ynevmerzhitsky/AccidentVisionSystem.git
cd AccidentVisionSystem
```

### 2. Create and Populate `.env`

Copy the example file and edit:

```bash
cp .env.example .env
```

### 3. Build and Launch Docker Containers

#### All services
```bash
docker-compose up --build -d
```

This will start:

* `web` (Django)
* `consumer` (Django command)
* `worker` (Celery)
* `db` (PostgreSQL)
* `rabbitmq` (RabbitMQ with management UI)

### 4. Run Database Migrations

#### Inside docker container
```bash
docker-compose exec web python manage.py migrate
```

### 5. Create a Superuser

#### Inside docker container
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Access the Services

* Django app: [http://localhost:8000](http://localhost:8000)
* RabbitMQ management: [http://localhost:15672](http://localhost:15672) (guest/guest)

### 7. Stopping the System

```bash
docker-compose down
```

## Step-by-Step Setup Instructions (App without docker)

### Prerequisites

* Docker >= 20.10
* Docker Compose >= 1.29
* Git
* Python >= 3.8

### 1. Clone the Repository

```bash
git clone https://github.com/ynevmerzhitsky/AccidentVisionSystem.git
cd AccidentVisionSystem
```

### 2. Set Up a Virtual Environment
```bash
python3 --version
python3 -m venv venv
venv\Scripts\activate # On Unix source venv/bin/activate
```

### 3. Create and Populate `.env`

Create a new file .env
Fill in values:

```ini
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
POSTGRES_DB=accidentvision
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
RABBITMQ_DEFAULT_VHOST=/
RABBITMQ_HOST=127.0.0.1
RABBITMQ_PORT=5672
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch Docker Containers

#### Only RabbitMQ and PostgreSQL
```bash
docker-compose up -d db rabbitmq
```

This will start:
* `db` (PostgreSQL)
* `rabbitmq` (RabbitMQ with management UI)

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Django Server

```bash
python manage.py runserver
```

### 6. Run the Django command to consume messages from task_result queue

```bash
python manage.py consume_results
```

### 6.  Start background worker to consume messages from task queue

```bash
celery -A accidentvision worker --loglevel=info
```

### 6. Access the Services

* Django app: [http://localhost:8000](http://localhost:8000)
* RabbitMQ management: [http://localhost:15672](http://localhost:15672) (guest/guest)

### 7. Stopping the RabbitMQ and PostgreSQL

```bash
docker-compose down
```

## Development

### Database Migrations

In Django, whenever you change your models (add fields, create new models, etc.), you follow this two-step process:

Create migration files tracking your model changes:

App Locally:
```bash
python manage.py makemigrations
```

OR

With app in Docker container:
```bash
docker-compose exec web python manage.py makemigrations
```

This inspects all installed apps’ models.py files and writes new migration scripts into each app’s migrations/ directory. 


Apply those migrations to update your database schema:

App Locally:
```bash
python manage.py migrate
```

OR

With app in Docker container:
```bash
docker-compose exec web python manage.py migrate
```

This runs the generated migration scripts in sequence, creating or altering tables in PostgreSQL so they match your current models
