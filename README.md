# 📚 Adaptive Learning Schedule Planner

An intelligent web-based study planner that automatically generates a personalized study schedule based on exam dates, subject difficulty, and available study time. It helps students prioritize important subjects, track daily progress, and stay organized throughout their exam preparation.

---

## 📸 Preview

![Adaptive Learning Schedule Planner](screenshots/preview.png)

---

## ✨ Features

- 📅 Adaptive daily study schedule generation
- ⏰ Smart time allocation based on exam urgency
- 📚 Subject management (Add & Delete)
- 📊 Dashboard with study statistics
- ✅ Daily study session tracking
- 📈 Real-time progress bar
- 📝 Weekly study planner
- 🎯 Difficulty-based scheduling
- 📆 Upcoming exams overview
- 💾 Persistent data storage using SQLite

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | SQLite |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
Adaptive-Learning-Schedule-Planner/
│
├── app/
│   ├── routes.py
│   ├── scheduler.py
│   ├── database.py
│   ├── models.py
│   └── __init__.py
│
├── templates/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── database/
│
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/SamRepository25/Adaptive-Learning-Schedule-Planner.git
```

### Navigate to the project

```bash
cd Adaptive-Learning-Schedule-Planner
```

### Create a virtual environment (Optional)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

### Open in your browser

```
http://127.0.0.1:5000
```

---

## 🎯 How It Works

1. Add your subjects with exam dates and difficulty.
2. Set your available daily study time.
3. The planner automatically calculates study priorities.
4. A personalized daily schedule is generated.
5. Mark completed study sessions to track progress.
6. View your weekly study plan and upcoming exams.

---

## 📊 Scheduling Logic

The planner calculates study priority using:

- Exam date proximity
- Subject difficulty
- Available daily study time

Subjects with higher urgency receive more study time, ensuring efficient exam preparation.

---

## 🚀 Future Improvements

- 🔐 User Authentication
- ☁️ Cloud Database Support
- 📱 Fully Responsive Mobile UI
- 🤖 AI-powered Study Recommendations
- 📅 Google Calendar Integration
- 🔔 Email & Push Notifications
- 🌙 Dark Mode
- 📈 Advanced Analytics Dashboard
- 📥 Export Study Schedule as PDF

---

## 🤝 Contributing

Contributions are welcome!

1. Fork this repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License**.

See the **LICENSE** file for more information.

---

## 👨‍💻 Author

**B. Simak Ahmed**

- GitHub: https://github.com/SamRepository25

---

## ⭐ Support

If you found this project useful, please consider giving it a **⭐ Star** on GitHub. Your support helps improve and grow the project.
