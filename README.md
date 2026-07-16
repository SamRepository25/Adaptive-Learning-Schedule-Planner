# Adaptive Learning Schedule Planner

A study planner that automatically calculates how much daily time to allocate
to each subject based on exam proximity and difficulty — no manual prioritizing needed.

## How it works

Each subject has an **urgency score**: `difficulty / days_left`. Subjects
closer to their exam date, or harder in difficulty, get a higher score. The
app then distributes a configurable daily study budget (120 minutes by
default) proportionally across all subjects based on their urgency share —
recalculated fresh every time the page loads or the daily time input changes.

## Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Deployment:** Render (Gunicorn WSGI server)

## Features

- Dashboard with live stat cards (subjects, daily time, upcoming exams, sessions today)
- Add / delete subjects with name, exam date, and difficulty (Easy / Medium / Hard)
- Server-side validation (duplicate names, invalid dates, past dates rejected)
- Adaptive daily schedule generation based on urgency, not stored priority
- Today's timetable with real clock times and breaks between sessions
- Progress tracking — mark sessions complete, live progress bar
- Upcoming exams list, sorted by nearest date
- Weekly study plan (round-robin distribution weighted by urgency)
- Configurable daily study time (30–600 minutes, default 120)
- Color-coded urgency indicators (sage / amber / red)
- Graceful error handling for network and server failures

## Project Structure

```
ALP/
├── app/
│   ├── __init__.py        # App factory
│   ├── models.py          # Subject and SessionCompletion models
│   ├── routes.py          # API + page routes
│   ├── scheduler.py       # Urgency scoring, schedule, timetable, weekly plan
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/
│       ├── base.html
│       └── index.html
├── config.py
├── run.py                 # Local dev entry point
├── Procfile                # Render start command
├── requirements.txt
└── .gitignore
```

## Local Setup

```bash
git clone <your-repo-url>
cd ALP
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

If you're updating from an older version of this project with a different
database schema, delete `instance/planner.db` before running — it will be
recreated automatically with the current schema.

## API Endpoints

| Method | Endpoint                          | Description                              |
|--------|-------------------------------------|-------------------------------------------|
| GET    | `/api/subjects`                    | List all subjects                          |
| POST   | `/api/subjects`                    | Add a subject                              |
| DELETE | `/api/subjects/<id>`               | Delete a subject                            |
| GET    | `/api/schedule?daily_minutes=`     | Urgency-sorted schedule with allocated time |
| GET    | `/api/timetable?daily_minutes=`    | Today's timed study sessions                |
| POST   | `/api/sessions/<subject_id>/complete` | Toggle a session's completion for today  |
| GET    | `/api/dashboard?daily_minutes=`    | Summary stats for the dashboard             |
| GET    | `/api/exams/upcoming`              | Upcoming exams, sorted by date              |
| GET    | `/api/weekly-plan`                 | Round-robin weekly study distribution       |

`daily_minutes` is optional on every endpoint that accepts it; it defaults to
120 and is clamped to the 30–600 range.

## Render Deployment

1. Push this project to GitHub.
2. Go to [render.com](https://render.com) → **New** → **Web Service**.
3. Connect your GitHub repo.
4. Configure:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn "app:create_app()"` (or leave blank — Render reads the `Procfile`)
5. Add an environment variable `SECRET_KEY` set to a random string.
6. Deploy, then visit the generated `https://<your-app>.onrender.com` URL.

## Known Limitation

Render's free tier uses an **ephemeral filesystem** — the SQLite database
resets on each redeploy/restart. This is an intentional tradeoff for a
portfolio-scale project; a production version would use Render's persistent
disks or migrate to PostgreSQL.

## License

MIT
