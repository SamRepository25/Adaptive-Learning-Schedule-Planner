from datetime import date
from app.models import Subject

DAILY_BUDGET_MINUTES = 120  # total study time per day, configurable


def calculate_urgency(subject: Subject, today: date = None) -> float:
    """Higher score = more urgent. Combines exam proximity and difficulty."""
    today = today or date.today()
    days_left = (subject.exam_date - today).days
    days_left = max(days_left, 1)  # avoid division by zero / negative for overdue exams
    return subject.difficulty / days_left


def generate_schedule(daily_budget_minutes: int = DAILY_BUDGET_MINUTES) -> list[dict]:
    """
    Returns a list of dicts, one per subject, with computed urgency,
    days_left, and allocated study minutes for today.
    """
    subjects = Subject.query.all()

    if not subjects:
        return []

    today = date.today()
    scored = []
    for subject in subjects:
        urgency = calculate_urgency(subject, today)
        days_left = max((subject.exam_date - today).days, 0)
        scored.append({
            "subject": subject,
            "urgency": urgency,
            "days_left": days_left
        })

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

    # Most urgent first
    schedule.sort(key=lambda x: x["urgency_score"], reverse=True)
    return schedule