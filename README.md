# Task Manager

A full-stack task management application built with a **Django REST Framework** backend and a **Next.js** frontend.

---

## Tech Stack

### Backend
- **Python** / **Django 6**
- **Django REST Framework** — REST API with token-based authentication
- **PostgreSQL** — Database
- **django-cors-headers** — CORS support
- **python-decouple** — Environment variable management

### Frontend
- **Next.js 16** (App Router)
- **React 19**
- **TypeScript**
- **Tailwind CSS 4**

---

## Project Structure

```
myproject/
├── base/               # Django app — models, views, serializers, URLs
├── myproject/          # Django project settings & root URL config
├── frontend/           # Next.js frontend application
│   └── src/
│       ├── app/        # App Router pages (login, register, home)
│       ├── components/ # Reusable UI components
│       └── context/    # React context (AuthContext)
├── manage.py
└── requirements.txt
```

---

## Features

- User **registration** and **login** with token authentication
- Full **CRUD** for tasks (create, read, update, delete)
- Toggle task **completion status**
- Filter tasks by **completed** or **pending**
- Tasks are scoped per authenticated user

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register/` | Register a new user | No |
| POST | `/api/login/` | Login and receive token | No |
| GET | `/api/tasks/` | List all tasks | Yes |
| POST | `/api/tasks/` | Create a new task | Yes |
| GET | `/api/tasks/{id}/` | Retrieve a task | Yes |
| PUT | `/api/tasks/{id}/` | Update a task | Yes |
| PATCH | `/api/tasks/{id}/` | Partially update a task | Yes |
| DELETE | `/api/tasks/{id}/` | Delete a task | Yes |
| POST | `/api/tasks/{id}/toggle/` | Toggle completion status | Yes |
| GET | `/api/tasks/completed/` | List completed tasks | Yes |
| GET | `/api/tasks/pending/` | List pending tasks | Yes |
| GET | `/api/users/me/` | Get current user info | Yes |

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL

---

### Backend Setup

1. **Clone the repository and navigate to the project root:**
   ```bash
   git clone <repo-url>
   cd myproject
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=myproject_db
   DB_USER=postgres
   DB_PASSWORD=your-db-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Create the database** (in PostgreSQL):
   ```sql
   CREATE DATABASE myproject_db;
   ```

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000/api/`.

---

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**

   Create a `.env.local` file inside `frontend/`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`.

---

## Authentication

The API uses **token-based authentication**. After logging in or registering, include the token in the `Authorization` header for all protected requests:

```
Authorization: Token <your-token>
```

