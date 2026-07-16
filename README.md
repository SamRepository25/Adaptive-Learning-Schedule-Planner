# 📚 Adaptive Learning Schedule Planner

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" />
  <img src="https://img.shields.io/badge/Flask-3.x-black?logo=flask" />
  <img src="https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite" />
  <img src="https://img.shields.io/badge/HTML5-orange?logo=html5" />
  <img src="https://img.shields.io/badge/CSS3-blue?logo=css3" />
  <img src="https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

<p align="center">
A Flask-based study planner that intelligently generates personalized daily study schedules based on exam dates and subject difficulty.
</p>

---

## 🚀 Live Demo

🌐 **https://adaptivelearningscheduler.onrender.com**

---

## 📖 Overview

Adaptive Learning Schedule Planner helps students organize their study time automatically.

Instead of manually deciding what to study first, the application calculates an urgency score for each subject and generates a balanced daily study schedule.

---

## ✨ Features

- 📚 Add study subjects
- 📅 Set exam dates
- 🎯 Select difficulty (Easy / Medium / Hard)
- ⚡ Automatic urgency calculation
- 📈 Dynamic study schedule generation
- 🗑 Delete subjects instantly
- 🔒 Server-side validation
- 💾 SQLite database
- 🌐 REST API
- 📱 Responsive interface
- ☁️ Deployed on Render

---

## 🧠 Scheduling Algorithm

The urgency score is calculated using:

```text
Urgency Score = Difficulty ÷ Days Remaining
```

Subjects with:

- Earlier exam dates
- Higher difficulty

receive more study time.

Example:

| Subject | Difficulty | Days Left | Priority |
|---------|-----------:|----------:|---------:|
| DBMS | Hard | 4 | High |
| Java | Medium | 10 | Medium |
| Python | Easy | 20 | Low |

The application distributes a fixed **120-minute daily study budget** proportionally based on each subject's urgency score.

---

## 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Server | Gunicorn |
| Hosting | Render |

---

## 📂 Project Structure

```text
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

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/SamRepository25/Adaptive-Learning-Schedule-Planner.git
```

Move into the project

```bash
cd Adaptive-Learning-Schedule-Planner
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python run.py
```

Open

```text
http://127.0.0.1:5000
```

---

## 💻 Usage

1. Add a subject.
2. Select its exam date.
3. Choose the difficulty.
4. Click **Add Subject**.
5. View the automatically generated study schedule.

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/subjects` | Get all subjects |
| POST | `/api/subjects` | Add a subject |
| DELETE | `/api/subjects/<id>` | Delete a subject |
| GET | `/api/schedule` | Generate study schedule |

---

## 📸 Screenshots

> Add screenshots of your application here after deployment.

---

## 🔮 Future Improvements

- User authentication
- Dark mode
- Calendar integration
- Email reminders
- Progress analytics
- Export schedule to PDF
- PostgreSQL support
- Mobile app

---

## 📚 Learning Outcomes

This project helped me gain practical experience with:

- Flask
- SQLAlchemy ORM
- REST APIs
- SQLite
- JavaScript Fetch API
- CRUD Operations
- Git & GitHub
- Render Deployment

---

## 👨‍💻 Author

**B Simak Ahmed**

GitHub: https://github.com/SamRepository25

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ If you found this project useful, consider giving it a Star!
