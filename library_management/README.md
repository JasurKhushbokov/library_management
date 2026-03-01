# Library Management System

A Django-based Library Management System for managing books, authors, categories, and borrow records. The project includes user authentication, book borrowing functionality, wishlists, and a complete Docker setup for development and production.

## Features

### User Features
- User registration and authentication
- Browse books, authors, and categories
- Borrow books from the library
- Return borrowed books
- Add books to wishlist
- View borrowing history

### Admin Features
- Django admin panel for content management
- Manage books (create, read, update, delete)
- Manage authors
- Manage categories
- View and manage borrow records

### Technical Features
- PostgreSQL database
- Docker containerization
- Nginx reverse proxy
- Gunicorn production server
- Environment-based configuration

## Technologies Used

| Category | Technology |
|----------|------------|
| Backend | Django 5.2 |
| Database | PostgreSQL 16 |
| Web Server | Gunicorn |
| Reverse Proxy | Nginx |
| Containerization | Docker & Docker Compose |
| Python | 3.12 |

## Project Structure

```
library_management/
├── library/                    # Django app
│   ├── admin.py              # Admin configuration
│   ├── models.py            # Database models
│   ├── views.py             # Business logic
│   ├── forms.py             # Forms
│   └── urls.py              # URL routing
├── library_management/        # Django project settings
├── templates/                # HTML templates
├── static/                   # Static files (CSS)
├── media/                    # User-uploaded files
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Production compose
├── docker-compose.dev.yml    # Development compose
├── nginx.conf               # Nginx configuration
└── requirements.txt         # Python dependencies
```

## Local Setup

### Prerequisites
- Python 3.12+
- PostgreSQL (optional, can use Docker)

### Option 1: Running Locally

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create .env file:**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
```

7. **Access the application:**
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

### Option 2: Using Docker (Development)

1. **Start containers:**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

2. **Access the application:**
- Website: http://localhost:8000
- Admin: http://localhost:8000/admin

### Option 3: Using Docker (Production)

1. **Start containers:**
```bash
docker-compose up --build
```

2. **Access the application:**
- Website: http://localhost
- Admin: http://localhost/admin

## Deployment

### Production Deployment with Docker

1. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with production values
```

2. **Update ALLOWED_HOSTS in .env:**
```
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

3. **Build and start:**
```bash
docker-compose up --build -d
```

4. **Create superuser:**
```bash
docker-compose exec web python manage.py createsuperuser
```

### Nginx Configuration

The Nginx configuration (`nginx.conf`) provides:
- Reverse proxy to Django/Gunicorn
- Static file serving (30-day cache)
- Media file serving (7-day cache)
- Gzip compression
- Request timeouts

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | False |
| `ALLOWED_HOSTS` | Allowed hostnames | localhost,127.0.0.1 |
| `DB_NAME` | PostgreSQL database name | library_db |
| `DB_USER` | PostgreSQL username | postgres |
| `DB_PASSWORD` | PostgreSQL password | Required |
| `DB_HOST` | Database host | db |
| `DB_PORT` | Database port | 5432 |
| `NGINX_PORT` | Nginx port | 80 |

### Example .env File

```env
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432
NGINX_PORT=80
```

## API Endpoints

| Endpoint | Description | Access |
|----------|-------------|--------|
| `/` | Home page | Public |
| `/accounts/register/` | User registration | Public |
| `/accounts/login/` | User login | Public |
| `/accounts/logout/` | User logout | Authenticated |
| `/books/` | Book list | Public |
| `/books/<id>/` | Book detail | Public |
| `/books/create/` | Add book | Admin only |
| `/books/<id>/update/` | Edit book | Admin only |
| `/books/<id>/delete/` | Delete book | Admin only |
| `/books/<id>/borrow/` | Borrow book | Authenticated |
| `/authors/` | Author list | Public |
| `/categories/` | Category list | Public |
| `/my-borrowings/` | User's borrowed books | Authenticated |
| `/wishlist/` | User's wishlist | Authenticated |
| `/admin/` | Django admin | Staff only |

## Database Models

### Author
- name (CharField)
- biography (TextField)
- date_of_birth (DateField)

### Category
- name (CharField)
- description (TextField)

### Book
- title (CharField)
- isbn (CharField, unique)
- published_date (DateField)
- description (TextField)
- cover_image (ImageField)
- available_copies (PositiveIntegerField)
- author (ForeignKey to Author)
- categories (ManyToManyField to Category)

### BorrowRecord
- user (ForeignKey to User)
- book (ForeignKey to Book)
- borrowed_at (DateTimeField)
- due_date (DateField)
- returned_at (DateTimeField)
- status (CharField: borrowed/returned/overdue)

### Wishlist
- user (OneToOneField to User)
- books (ManyToManyField to Book)

## Security Notes

- Change `SECRET_KEY` in production
- Use strong database passwords
- Keep `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` properly
- Use HTTPS in production

## License

This project is for educational purposes.


