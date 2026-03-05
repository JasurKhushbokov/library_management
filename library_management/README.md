# Library Management System

**Student ID:** 00016171  
**Module:** DSCC / DevOps & Software Continuous Delivery  
**University:** Westminster International University in Tashkent

A full-stack Django-based Library Management System for managing books, authors, categories, and borrow records. The project features user authentication, book borrowing, wishlists, and is fully containerized with Docker. It is deployed to an Azure Virtual Machine via a CI/CD pipeline using GitHub Actions.

**Live Application:** http://135.235.139.102  
**GitHub Repository:** https://github.com/JasurKhushbokov/library_management

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [URL Endpoints](#url-endpoints)
- [Local Setup](#local-setup)
- [Docker Setup](#docker-setup)
- [CI/CD Pipeline](#cicd-pipeline)
- [Azure Deployment](#azure-deployment)
- [Environment Variables](#environment-variables)
- [Security](#security)

---

## Features

### User Features

- User registration and login/logout authentication
- Browse books, authors, and categories
- Search and filter books
- Borrow books from the library
- Return borrowed books
- View personal borrowing history
- Add/remove books to/from a personal wishlist

### Admin Features

- Full Django admin panel for content management
- CRUD operations for books, authors, and categories
- View and manage all borrow records

### Technical Features

- Multi-stage Docker build (builder + production)
- Non-root Docker container user for security
- PostgreSQL database with health checks
- Nginx reverse proxy with static/media file caching and gzip compression
- Gunicorn WSGI production server (2 workers)
- Container health check endpoint (`/health/`)
- CI/CD pipeline with GitHub Actions (test → build → deploy)
- Automated deployment to Azure VM via SSH

---

## Technologies Used

| Category             | Technology              | Version     |
| -------------------- | ----------------------- | ----------- |
| Backend Framework    | Django                  | 5.2.4       |
| Programming Language | Python                  | 3.12        |
| Database             | PostgreSQL              | 16 (Alpine) |
| WSGI Server          | Gunicorn                | 23.0.0      |
| Reverse Proxy        | Nginx                   | Alpine      |
| Containerization     | Docker & Docker Compose | Latest      |
| CI/CD                | GitHub Actions          | v4          |
| Cloud Platform       | Microsoft Azure         | VM (Ubuntu) |
| Image Processing     | Pillow                  | 12.1.1      |
| Env Management       | python-dotenv           | 1.1.0       |
| Database Adapter     | psycopg2-binary         | 2.9.11      |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Azure VM (Ubuntu)                    │
│                                                          │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐   │
│  │  Nginx   │───>│ Django +     │───>│  PostgreSQL   │   │
│  │ (Port 80)│    │ Gunicorn     │    │  (Port 5432)  │   │
│  │          │    │ (Port 8000)  │    │               │   │
│  └──────────┘    └──────────────┘    └───────────────┘   │
│       │                                                  │
│  Static Files    Media Files                             │
│  (30-day cache)  (7-day cache)                           │
└──────────────────────────────────────────────────────────┘
         ▲
         │ HTTP (Port 80)
         │
    ┌────┴─────┐
    │  Client  │
    │ (Browser)│
    └──────────┘
```

### CI/CD Pipeline Flow

```
┌──────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────────┐
│ Developer │────>│  GitHub  │────>│   GitHub     │────>│  Azure VM    │
│ git push  │     │   Repo   │     │   Actions    │     │  Deployment  │
└──────────┘     └──────────┘     │              │     └──────────────┘
                                   │ 1. Test      │
                                   │ 2. Build     │
                                   │ 3. Deploy    │
                                   └─────────────┘
```

---

## Project Structure

```
DSCC_CW1_00016171/
├── .github/
│   └── workflows/
│       └── ci-cd.yml               # GitHub Actions CI/CD pipeline
├── library_management/             # Django project root
│   ├── library/                    # Main Django app
│   │   ├── __init__.py
│   │   ├── admin.py               # Admin site configuration
│   │   ├── apps.py                # App configuration
│   │   ├── forms.py               # Django forms (Registration, Book, Author, Category)
│   │   ├── models.py              # Database models (Book, Author, Category, BorrowRecord, Wishlist)
│   │   ├── urls.py                # URL routing with 20+ endpoints
│   │   ├── views.py               # View functions (business logic)
│   │   └── migrations/            # Database migrations
│   │       ├── 0001_initial.py
│   │       └── 0002_wishlist.py
│   ├── library_management/         # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py            # Project settings (env-based config)
│   │   ├── urls.py                # Root URL configuration
│   │   ├── wsgi.py                # WSGI entry point
│   │   └── asgi.py                # ASGI entry point
│   ├── templates/                  # HTML templates
│   │   ├── base.html              # Base template with navigation
│   │   └── library/               # App-specific templates
│   │       ├── home.html          # Landing page with stats
│   │       ├── book_list.html     # Book catalog
│   │       ├── book_detail.html   # Individual book view
│   │       ├── book_form.html     # Add/edit book form
│   │       ├── book_confirm_delete.html
│   │       ├── author_list.html
│   │       ├── author_detail.html
│   │       ├── author_form.html
│   │       ├── author_confirm_delete.html
│   │       ├── category_list.html
│   │       ├── category_detail.html
│   │       ├── category_form.html
│   │       ├── category_confirm_delete.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── my_borrowings.html
│   │       └── wishlist.html
│   ├── static/
│   │   └── css/
│   │       └── style.css          # Custom styles
│   ├── media/
│   │   └── covers/                # Uploaded book cover images
│   ├── Dockerfile                 # Multi-stage Docker build
│   ├── docker-compose.yml         # Default compose configuration
│   ├── docker-compose.dev.yml     # Development compose (with hot reload)
│   ├── docker-compose.prod.yml    # Production compose (Nginx + Gunicorn + PostgreSQL)
│   ├── nginx.conf                 # Nginx reverse proxy configuration
│   ├── manage.py                  # Django management script
│   ├── requirements.txt           # Python dependencies
│   ├── deploy-azure.sh            # Manual Azure deployment script
│   ├── set_password.py            # Admin password reset utility
│   ├── .env                       # Environment variables (not tracked in git)
│   ├── .env.example               # Example environment variables
│   ├── .gitignore                 # Git ignore rules
│   └── .dockerignore              # Docker ignore rules
├── README.md                      # This file
└── requirements.txt               # Root-level requirements reference
```

---

## Database Models

### Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│    Author    │       │      Book        │       │   Category   │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)          │       │ id (PK)      │
│ name         │◄──────│ author (FK)      │──────►│ name         │
│ biography    │  1:N  │ title            │  M:N  │ description  │
│ date_of_birth│       │ isbn (unique)    │       └──────────────┘
└──────────────┘       │ published_date   │
                       │ description      │
                       │ cover_image      │
                       │ available_copies │
                       └───────┬──────────┘
                               │ 1:N
                       ┌───────┴──────────┐
                       │  BorrowRecord    │       ┌──────────────┐
                       ├──────────────────┤       │   Wishlist   │
                       │ id (PK)          │       ├──────────────┤
                       │ user (FK → User) │       │ id (PK)      │
                       │ book (FK → Book) │       │ user (1:1)   │
                       │ borrowed_at      │       │ books (M:N)  │
                       │ due_date         │       │ created_at   │
                       │ returned_at      │       └──────────────┘
                       │ status           │
                       └──────────────────┘
```

### Model Details

| Model            | Field              | Type                       | Constraints                                |
| ---------------- | ------------------ | -------------------------- | ------------------------------------------ |
| **Author**       | `name`             | CharField(200)             | Required                                   |
|                  | `biography`        | TextField                  | Optional                                   |
|                  | `date_of_birth`    | DateField                  | Optional                                   |
| **Category**     | `name`             | CharField(100)             | Required                                   |
|                  | `description`      | TextField                  | Optional                                   |
| **Book**         | `title`            | CharField(200)             | Required                                   |
|                  | `isbn`             | CharField(13)              | Unique                                     |
|                  | `published_date`   | DateField                  | Optional                                   |
|                  | `description`      | TextField                  | Optional                                   |
|                  | `cover_image`      | ImageField                 | Optional, uploads to `covers/`             |
|                  | `available_copies` | PositiveIntegerField       | Default: 1                                 |
|                  | `author`           | ForeignKey → Author        | CASCADE                                    |
|                  | `categories`       | ManyToManyField → Category |                                            |
| **BorrowRecord** | `user`             | ForeignKey → User          | CASCADE                                    |
|                  | `book`             | ForeignKey → Book          | CASCADE                                    |
|                  | `borrowed_at`      | DateTimeField              | Auto-set on create                         |
|                  | `due_date`         | DateField                  | Required                                   |
|                  | `returned_at`      | DateTimeField              | Optional                                   |
|                  | `status`           | CharField(20)              | Choices: `borrowed`, `returned`, `overdue` |
| **Wishlist**     | `user`             | OneToOneField → User       | CASCADE                                    |
|                  | `books`            | ManyToManyField → Book     |                                            |
|                  | `created_at`       | DateTimeField              | Auto-set on create                         |

---

## URL Endpoints

| Endpoint                   | Method    | Description                                  | Access        |
| -------------------------- | --------- | -------------------------------------------- | ------------- |
| `/`                        | GET       | Home page with book stats and featured books | Public        |
| `/register/`               | GET, POST | User registration                            | Public        |
| `/login/`                  | GET, POST | User login                                   | Public        |
| `/logout/`                 | POST      | User logout                                  | Authenticated |
| `/books/`                  | GET       | Book catalog with search                     | Public        |
| `/books/<id>/`             | GET       | Book detail page                             | Public        |
| `/books/create/`           | GET, POST | Add a new book                               | Admin only    |
| `/books/<id>/update/`      | GET, POST | Edit a book                                  | Admin only    |
| `/books/<id>/delete/`      | GET, POST | Delete a book                                | Admin only    |
| `/books/<id>/borrow/`      | POST      | Borrow a book                                | Authenticated |
| `/authors/`                | GET       | Author list                                  | Public        |
| `/authors/<id>/`           | GET       | Author detail with their books               | Public        |
| `/authors/create/`         | GET, POST | Add a new author                             | Admin only    |
| `/authors/<id>/update/`    | GET, POST | Edit an author                               | Admin only    |
| `/authors/<id>/delete/`    | GET, POST | Delete an author                             | Admin only    |
| `/categories/`             | GET       | Category list                                | Public        |
| `/categories/<id>/`        | GET       | Category detail with books                   | Public        |
| `/categories/create/`      | GET, POST | Add a new category                           | Admin only    |
| `/categories/<id>/update/` | GET, POST | Edit a category                              | Admin only    |
| `/categories/<id>/delete/` | GET, POST | Delete a category                            | Admin only    |
| `/my-borrowings/`          | GET       | User's borrowing history                     | Authenticated |
| `/borrow/<id>/return/`     | POST      | Return a borrowed book                       | Authenticated |
| `/wishlist/`               | GET       | User's wishlist                              | Authenticated |
| `/wishlist/add/<id>/`      | POST      | Add book to wishlist                         | Authenticated |
| `/wishlist/remove/<id>/`   | POST      | Remove book from wishlist                    | Authenticated |
| `/health/`                 | GET       | Health check endpoint (JSON)                 | Public        |
| `/admin/`                  | GET       | Django admin panel                           | Staff only    |

---

## Local Setup

### Prerequisites

- Python 3.12+
- PostgreSQL 16+ (or use Docker)
- Git

### Option 1: Running Locally (without Docker)

1. **Clone the repository:**

```bash
git clone https://github.com/JasurKhushbokov/library_management.git
cd library_management/library_management
```

2. **Create and activate virtual environment:**

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create environment file:**

```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run database migrations:**

```bash
python manage.py migrate
```

6. **Create admin superuser:**

```bash
python manage.py createsuperuser
```

7. **Start the development server:**

```bash
python manage.py runserver
```

8. **Access the application:**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

---

## Docker Setup

### Development Mode

Development mode mounts local files for hot-reload:

```bash
cd library_management
docker-compose -f docker-compose.dev.yml up --build
```

- Website: http://localhost:8000
- Admin: http://localhost:8000/admin

### Production Mode (Local)

Production mode uses Nginx reverse proxy + Gunicorn:

```bash
cd library_management
docker-compose -f docker-compose.prod.yml up --build -d
```

- Website: http://localhost (port 80)
- Admin: http://localhost/admin

### Docker Architecture

```
docker-compose.prod.yml
├── web (library-app:latest)
│   ├── Django + Gunicorn on port 8000
│   ├── Multi-stage build (builder → production)
│   ├── Non-root user (appuser)
│   ├── Auto-runs migrations on startup
│   └── Health check via /health/ endpoint
├── db (postgres:16-alpine)
│   ├── PostgreSQL database
│   ├── Persistent volume (postgres_data)
│   └── Health check via pg_isready
└── nginx (nginx:alpine)
    ├── Reverse proxy to web:8000
    ├── Serves static files (30-day cache)
    ├── Serves media files (7-day cache)
    ├── Gzip compression enabled
    └── Exposed on port 80
```

### Dockerfile (Multi-Stage Build)

| Stage                   | Purpose                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------ |
| **Stage 1: Builder**    | Installs gcc, libpq-dev, creates venv, installs Python dependencies                  |
| **Stage 2: Production** | Copies venv from builder, copies project files, creates non-root user, runs Gunicorn |

---

## CI/CD Pipeline

The project uses **GitHub Actions** for continuous integration and continuous deployment. The workflow is defined in `.github/workflows/ci-cd.yml` and triggers on every push to the `master` branch.

### Pipeline Overview

```
Push to master
      │
      ▼
┌─────────────────┐    ┌───────────────────┐    ┌──────────────────────┐
│  Job 1: Test    │───>│  Job 2: Build     │───>│  Job 3: Deploy       │
│  (34 seconds)   │    │  (35 seconds)     │    │  (1 min 35 sec)      │
├─────────────────┤    ├───────────────────┤    ├──────────────────────┤
│ ✓ Checkout code │    │ ✓ Checkout code   │    │ ✓ Checkout code      │
│ ✓ Setup Python  │    │ ✓ Build Docker    │    │ ✓ Download artifact  │
│   3.12          │    │   image           │    │ ✓ Validate secrets   │
│ ✓ Install deps  │    │ ✓ Verify image    │    │ ✓ Setup SSH key      │
│ ✓ Django checks │    │ ✓ Save image      │    │ ✓ Transfer image     │
│ ✓ Run migrations│    │   as .tar         │    │   to Azure VM        │
│ ✓ Run tests     │    │ ✓ Upload artifact │    │ ✓ Transfer configs   │
└─────────────────┘    └───────────────────┘    │ ✓ Deploy (docker     │
                                                │   load + compose up) │
                                                │ ✓ Verify deployment  │
                                                │ ✓ Cleanup SSH key    │
                                                └──────────────────────┘
```

### Job 1: Lint & Test

Runs on `ubuntu-latest` with a PostgreSQL 16 service container:

- **Checkout code** — Pulls the latest code from the repository
- **Set up Python 3.12** — Installs Python with pip caching
- **Install dependencies** — Installs Django, psycopg2, Pillow, etc.
- **Run Django checks** — Validates models, settings, and configurations
- **Run migrations** — Applies all database migrations to verify they work
- **Run tests** — Executes Django unit tests (`python manage.py test`)

### Job 2: Build Docker Image

Only runs if Job 1 passes:

- **Checkout code** — Pulls the repository
- **Build Docker image** — Builds the multi-stage production image
- **Verify image** — Confirms the image was created
- **Save Docker image** — Exports to `library-app.tar`
- **Upload artifact** — Stores the tar file for the deploy job

### Job 3: Deploy to Azure VM

Only runs if Job 2 passes AND the push is to `master`:

- **Download artifact** — Gets the Docker image tar from Job 2
- **Validate secrets** — Checks that `AZURE_VM_IP`, `AZURE_VM_USER`, `AZURE_SSH_KEY` are set
- **Set up SSH key** — Creates SSH key file and scans VM host keys
- **Transfer image** — SCP copies the Docker image tar to the Azure VM
- **Transfer configs** — Copies `docker-compose.prod.yml` and `nginx.conf`
- **Deploy** — SSHs into VM, loads the Docker image, stops old containers, starts new ones
- **Verify deployment** — Sends HTTP request to verify the app is running
- **Cleanup** — Removes the SSH key file

### Required GitHub Secrets

These must be configured in **Settings → Secrets and variables → Actions**:

| Secret          | Description                           | Example                              |
| --------------- | ------------------------------------- | ------------------------------------ |
| `AZURE_VM_IP`   | Public IP of the Azure VM             | `135.235.139.102`                    |
| `AZURE_VM_USER` | SSH username                          | `azureuser`                          |
| `AZURE_SSH_KEY` | Contents of the SSH private key (PEM) | `-----BEGIN RSA PRIVATE KEY-----...` |

---

## Azure Deployment

### Infrastructure

| Component      | Details                         |
| -------------- | ------------------------------- |
| Cloud Provider | Microsoft Azure                 |
| VM Size        | Standard B1s (1 vCPU, 1 GB RAM) |
| OS             | Ubuntu 24.04 LTS                |
| Public IP      | 135.235.139.102                 |
| Open Ports     | 22 (SSH), 80 (HTTP)             |
| Docker Engine  | Installed on VM                 |

### Manual Deployment (Alternative)

If not using CI/CD, deploy manually:

```bash
# 1. Build Docker image locally
docker build -t library-app:latest .

# 2. Save image to tar file
docker save -o library-app.tar library-app:latest

# 3. Copy files to Azure VM
scp -i azure-key.pem library-app.tar azureuser@135.235.139.102:~/
scp -i azure-key.pem docker-compose.prod.yml nginx.conf azureuser@135.235.139.102:~/

# 4. SSH into VM and deploy
ssh -i azure-key.pem azureuser@135.235.139.102

# On the VM:
sudo docker load -i library-app.tar
sudo docker compose -f docker-compose.prod.yml down
sudo docker compose -f docker-compose.prod.yml up -d
```

### Verify Deployment

```bash
# Check running containers
ssh -i azure-key.pem azureuser@135.235.139.102 "sudo docker ps"

# Check application health
curl http://135.235.139.102/health/

# View container logs
ssh -i azure-key.pem azureuser@135.235.139.102 "sudo docker logs library_web"
```

---

## Environment Variables

| Variable               | Description                                      | Default                             | Required         |
| ---------------------- | ------------------------------------------------ | ----------------------------------- | ---------------- |
| `SECRET_KEY`           | Django secret key for cryptographic signing      | Auto-generated (insecure)           | Yes (production) |
| `DEBUG`                | Enable Django debug mode                         | `False`                             | No               |
| `ALLOWED_HOSTS`        | Comma-separated list of allowed hostnames        | `localhost,127.0.0.1`               | Yes (production) |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated list of trusted origins for CSRF | `http://localhost,http://127.0.0.1` | Yes (production) |
| `DB_NAME`              | PostgreSQL database name                         | `library_db`                        | Yes              |
| `DB_USER`              | PostgreSQL username                              | `postgres`                          | Yes              |
| `DB_PASSWORD`          | PostgreSQL password                              | `postgres`                          | Yes              |
| `DB_HOST`              | Database hostname                                | `localhost` / `db` (Docker)         | Yes              |
| `DB_PORT`              | Database port                                    | `5432`                              | No               |

### Example .env File

```env
SECRET_KEY=your-secure-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,135.235.139.102
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1,http://135.235.139.102
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your-secure-database-password
DB_HOST=db
DB_PORT=5432
```

---

## Security

- **Non-root Docker user** — Application runs as `appuser` inside the container
- **Environment-based secrets** — All sensitive values stored in `.env` (not tracked in git)
- **GitHub Secrets** — SSH keys and VM credentials stored as encrypted GitHub Actions secrets
- **`.gitignore`** — Excludes `.env`, `*.pem`, `__pycache__/`, `*.tar`, `db.sqlite3`
- **`.dockerignore`** — Excludes `.git`, `.env`, `*.pem`, `venv/` from Docker builds
- **Multi-stage Docker build** — Build dependencies not included in production image
- **Django security checks** — `manage.py check --deploy` runs in CI pipeline
- **Password validators** — Django's built-in password validation enabled
- **CSRF protection** — Enabled with trusted origins configuration
- **Health check endpoint** — `/health/` returns JSON status for container monitoring

---

## License

This project is developed for educational purposes as part of the DSCC (DevOps & Software Continuous Delivery) module coursework at Westminster International University in Tashkent.
