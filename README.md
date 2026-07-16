# Adaptive Learning Schedule Planner

A study planner that automatically calculates how much daily time to allocate
to each subject based on exam proximity and difficulty — no manual prioritizing needed.

## How it works

Each subject has an **urgency score**: `difficulty / days_left`. Subjects
closer to their exam date, or harder in difficulty, get a higher score. The
app then distributes a fixed daily study budget (120 minutes) proportionally
across all subjects based on their urgency share — recalculated fresh every
time you load the schedule.

## Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Deployment:** Render (Gunicorn WSGI server)

## Features

- Add/delete subjects with name, exam date, and difficulty (Easy/Medium/Hard)
- Server-side validation (duplicate names, invalid dates, past dates rejected)
- Dynamic daily schedule generation based on urgency, not stored priority
- Visual urgency indicator (color-coded dot: sage → amber → red)
- Graceful error handling for network/server failures

## Project Structure