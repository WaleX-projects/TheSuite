# TheSuit

TheSuit is a modern all-in-one business operating system that helps companies manage HR, payroll, attendance, recruitment, employee data, and workplace operations from a single platform.

![TheSuit Preview](./screenshots/preview.png)

---

## ✨ Features

- Employee Management
- Payroll Processing
- Attendance Tracking
- Leave Management
- Recruitment System
- Analytics Dashboard
- Notifications & Alerts
- Role-Based Access Control
- Modern Responsive UI
- REST API Integration

---

## 🛠 Tech Stack

### Frontend
- React
- TypeScript
- TailwindCSS
- React Router
- Axios
- ShadCN UI

### Backend
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery

### DevOps
- AWS EC2
- Nginx
- Gunicorn
- Docker

---

## 🚀 Demo

Live demo: https://thesuit.netlify.app/

---

## 📸 Screenshots

### Dashboard
![Dashboard](./screenshots/dashboard.png)

### Payroll
![Payroll](./screenshots/payroll.png)

### Attendance
![Attendance](./screenshots/attendance.png)

---

## ⚡ Installation

### Run with Docker

From the repository root, build and start both services:

```bash
docker compose up --build
```

Open the frontend at [http://localhost:8080](http://localhost:8080). The Django API is available at [http://localhost:8000/api/](http://localhost:8000/api/). SQLite data, face-recognition data, and downloaded face models are stored in Docker volumes.

This Compose setup uses Django's development server and SQLite; it is intended for local development, not production.

### Clone Repository

```bash
git clone https://github.com/WaleX-projects/TheSuite-backend.git
cd thesuit
```
#-
