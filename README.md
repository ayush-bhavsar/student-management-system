# Student Management System

A complete beginner-friendly Student Management System built with **Python, Flask, SQLite, Flask-SQLAlchemy, Flask-Login and Bootstrap**.

## Features

- User registration and login
- Secure password hashing
- Protected student management pages
- Add, view, edit and delete students
- Search students by name, roll number, email or course
- Dashboard with total student and course counts
- Responsive Bootstrap UI
- SQLite database created automatically

## Project Structure

```text
student-management-system/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   └── students.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── students.html
│   ├── add_student.html
│   └── edit_student.html
├── static/
│   ├── css/style.css
│   └── js/script.js
└── database/
    └── .gitkeep
```

## Requirements

- Python 3.10+
- pip

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ayush-bhavsar/student-management-system.git
cd student-management-system
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set a secret key

For local testing the project has a development fallback. For real deployment, set the `SECRET_KEY` environment variable to a long random value.

Windows PowerShell:

```powershell
$env:SECRET_KEY="your-random-secret-key"
```

macOS/Linux:

```bash
export SECRET_KEY="your-random-secret-key"
```

### 5. Run the application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## How to Use

1. Open the application.
2. Register a new account.
3. Log in.
4. Add student records from **Add Student**.
5. View and search records from **Students**.
6. Use **Edit** or **Delete** to manage a record.
7. Use the dashboard for a quick overview.

## Database

The application uses SQLite. The database file is generated automatically at `database/students.db` on first run and is intentionally ignored by Git.

## Important Security Note

This project is suitable for learning and small local projects. Before production deployment, add CSRF protection, stronger validation, HTTPS, secure cookie settings, rate limiting, production secrets, and a production WSGI server.

## License

This project is available for educational and personal use.
