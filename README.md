# 📚 Adaptive Learning Schedule Planner

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![HTML5](https://img.shields.io/badge/HTML5-orange?logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-blue?logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)
![MIT License](https://img.shields.io/badge/License-MIT-green)

---

## 🌐 Live Demo

**https://adaptivelearningscheduler.onrender.com**

---

# 📖 Overview

Adaptive Learning Schedule Planner is a Flask-based web application that intelligently generates a personalized daily study schedule based on:

- 📅 Exam Date
- 📈 Subject Difficulty
- ⏳ Days Remaining

Instead of manually deciding which subject to study first, the application calculates an urgency score for every subject and automatically distributes your available study time.

---

# ✨ Features

- ✅ Add new subjects
- ✅ Select exam date
- ✅ Choose difficulty (Easy / Medium / Hard)
- ✅ Automatic urgency calculation
- ✅ Dynamic daily study schedule generation
- ✅ SQLite database
- ✅ Responsive UI
- ✅ Flask REST API
- ✅ Server-side validation
- ✅ Deployable on Render

---

# 🧠 How It Works

Every subject receives an **Urgency Score**.

```
Urgency Score = Difficulty Weight ÷ Days Remaining
```

Subjects with:

- Earlier exams
- Higher difficulty

receive more study time.

Example:

| Subject | Difficulty | Days Left | Priority |
|----------|-----------|----------:|---------:|
| DBMS | Hard | 4 | High |
| Java | Medium | 10 | Medium |
| Python | Easy | 20 | Low |

The application then distributes **120 minutes** of daily study time proportionally across all subjects.

---

# 🛠 Tech Stack

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript

## Backend

- Python
- Flask
- Flask-SQLAlchemy

## Database

- SQLite

## Deployment

- Gunicorn
- Render

---

# 📂 Project Structure

```
Adaptive-Learning-Schedule-Planner
│
├── app
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── main.js
│   │
│   ├── templates
│   │   ├── base.html
│   │   └── index.html
│   │
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── scheduler.py
│
├── config.py
├── Procfile
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/SamRepository25/Adaptive-Learning-Schedule-Planner.git
```

Move into the project

```bash
cd Adaptive-Learning-Schedule-Planner
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python run.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# 💻 Usage

1. Enter a subject name.
2. Select the exam date.
3. Choose the difficulty.
4. Click **Add Subject**.
5. View the automatically generated study schedule.

---

# 🌐 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/subjects` | Get all subjects |
| POST | `/api/subjects` | Add a subject |
| DELETE | `/api/subjects/<id>` | Delete a subject |
| GET | `/api/schedule` | Generate study schedule |

---

# 📸 Screenshots

## Home Page

_Add a screenshot here._

---

## Generated Study Schedule

_Add another screenshot here._

---

# 🚀 Future Improvements

- User authentication
- Dark mode
- Weekly planner
- Calendar integration
- Email reminders
- AI-powered schedule optimization
- Subject analytics dashboard
- Mobile responsiveness improvements
- Export schedule to PDF
- Cloud database support

---

# 📚 Learning Outcomes

This project helped me learn:

- Flask application architecture
- REST API development
- SQLAlchemy ORM
- CRUD operations
- SQLite database integration
- JavaScript Fetch API
- Responsive web design
- Git & GitHub workflow
- Render deployment with Gunicorn

---

# 👨‍💻 Author

**B Simak Ahmed**

Computer Science Engineering Student

GitHub: https://github.com/SamRepository25

---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you found this project useful, consider giving it a Star!
