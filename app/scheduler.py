from datetime import date, datetime, timedelta
from app.models import Subject

DEFAULT_DAILY_BUDGET_MINUTES = 120


def calculate_urgency(subject: Subject, today: date = None) -> float:
    """Higher score = more urgent. urgency = difficulty / days_left (min 1 day)."""
    today = today or date.today()
    days_left = (subject.exam_date - today).days
    days_left = max(days_left, 1)
    return subject.difficulty / days_left


def generate_schedule(daily_budget_minutes: int = DEFAULT_DAILY_BUDGET_MINUTES) -> list[dict]:
    """
    Returns one dict per subject with urgency score, days left, and allocated
    minutes for today, proportional to each subject's share of total urgency.
    Sorted most urgent first.
    """
    subjects = Subject.query.all()
    if not subjects:
        return []

    today = date.today()
    scored = []
    for subject in subjects:
        urgency = calculate_urgency(subject, today)
        days_left = max((subject.exam_date - today).days, 0)
        scored.append({"subject": subject, "urgency": urgency, "days_left": days_left})

    total_urgency = sum(item["urgency"] for item in scored)

    schedule = []
    for item in scored:
        share = item["urgency"] / total_urgency if total_urgency > 0 else 0
        allocated_minutes = round(share * daily_budget_minutes)
        entry = item["subject"].to_dict()
        entry.update({
            "urgency_score": round(item["urgency"], 4),
            "days_left": item["days_left"],
            "allocated_minutes": allocated_minutes
        })
        schedule.append(entry)

    schedule.sort(key=lambda x: x["urgency_score"], reverse=True)
    return schedule


def generate_timetable(daily_budget_minutes: int = DEFAULT_DAILY_BUDGET_MINUTES,
                        start_time_str: str = "18:00",
                        gap_minutes: int = 5) -> list[dict]:
    """Converts the urgency-sorted schedule into timed sessions with start/end clock times."""
    schedule = generate_schedule(daily_budget_minutes)
    if not schedule:
        return []

    try:
        current = datetime.strptime(start_time_str, "%H:%M")
    except ValueError:
        current = datetime.strptime("18:00", "%H:%M")

    timetable = []
    for item in schedule:
        minutes = item["allocated_minutes"]
        if minutes <= 0:
            continue
        end = current + timedelta(minutes=minutes)
        session = dict(item)
        session["start_time"] = current.strftime("%I:%M %p").lstrip("0")
        session["end_time"] = end.strftime("%I:%M %p").lstrip("0")
        timetable.append(session)
        current = end + timedelta(minutes=gap_minutes)

    return timetable


def generate_weekly_plan() -> dict:
    """Simple round-robin weekly distribution, weighted toward the most urgent subjects."""
    subjects = Subject.query.all()
    if not subjects:
        return {}

    today = date.today()
    scored = sorted(subjects, key=lambda s: calculate_urgency(s, today), reverse=True)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan = {day: [] for day in days}

    for i, subject in enumerate(scored):
        plan[days[i % 7]].append(subject.name)

    if scored:
        top_subject = scored[0]
        revision_day = days[2]
        plan[revision_day].append(f"{top_subject.name} Revision")

    return plan
