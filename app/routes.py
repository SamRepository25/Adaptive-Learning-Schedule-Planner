from datetime import datetime, date

from flask import Blueprint, render_template, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import Subject, SessionCompletion
from app.scheduler import generate_schedule, generate_timetable, generate_weekly_plan

main_bp = Blueprint("main", __name__)

VALID_DIFFICULTIES = (1, 3, 5)
DEFAULT_DAILY_BUDGET_MINUTES = 120
MIN_DAILY_MINUTES = 30
MAX_DAILY_MINUTES = 600


def _get_daily_budget_minutes():
    """Reads ?daily_minutes= from the query string, validates it, falls back to default."""
    raw = request.args.get("daily_minutes", type=int)
    if raw is None:
        return DEFAULT_DAILY_BUDGET_MINUTES
    if not (MIN_DAILY_MINUTES <= raw <= MAX_DAILY_MINUTES):
        return DEFAULT_DAILY_BUDGET_MINUTES
    return raw


# --- Page route ---

@main_bp.route("/")
def index():
    return render_template("index.html")


# --- Subject CRUD ---

@main_bp.route("/api/subjects", methods=["GET"])
def get_subjects():
    subjects = Subject.query.order_by(Subject.exam_date.asc()).all()
    return jsonify([s.to_dict() for s in subjects]), 200


@main_bp.route("/api/subjects", methods=["POST"])
def add_subject():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    name = (data.get("name") or "").strip()
    exam_date_raw = (data.get("exam_date") or "").strip()
    difficulty = data.get("difficulty")

    if not name:
        return jsonify({"error": "Subject name is required"}), 400
    if len(name) > 100:
        return jsonify({"error": "Subject name too long (max 100 chars)"}), 400

    if not exam_date_raw:
        return jsonify({"error": "Exam date is required"}), 400
    try:
        exam_date = datetime.strptime(exam_date_raw, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "exam_date must be in YYYY-MM-DD format"}), 400
    if exam_date < datetime.utcnow().date():
        return jsonify({"error": "exam_date cannot be in the past"}), 400

    if difficulty not in VALID_DIFFICULTIES:
        return jsonify({"error": "Difficulty must be 1 (Easy), 3 (Medium), or 5 (Hard)"}), 400

    if Subject.query.filter_by(name=name).first():
        return jsonify({"error": f"Subject '{name}' already exists"}), 409

    subject = Subject(name=name, exam_date=exam_date, difficulty=difficulty)
    db.session.add(subject)
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Failed to save subject. Please try again."}), 500

    return jsonify(subject.to_dict()), 201


@main_bp.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    subject = db.session.get(Subject, subject_id)
    if not subject:
        return jsonify({"error": f"Subject with id {subject_id} not found"}), 404

    db.session.delete(subject)
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Failed to delete subject. Please try again."}), 500

    return jsonify({"message": f"Subject '{subject.name}' deleted"}), 200


# --- Adaptive scheduling ---

@main_bp.route("/api/schedule", methods=["GET"])
def get_schedule():
    daily_minutes = _get_daily_budget_minutes()
    schedule = generate_schedule(daily_budget_minutes=daily_minutes)
    if not schedule:
        return jsonify({
            "message": "No subjects added yet",
            "schedule": [],
            "daily_minutes": daily_minutes
        }), 200
    return jsonify({"schedule": schedule, "daily_minutes": daily_minutes}), 200


@main_bp.route("/api/timetable", methods=["GET"])
def get_timetable():
    daily_minutes = _get_daily_budget_minutes()
    timetable = generate_timetable(daily_budget_minutes=daily_minutes)
    today = date.today()

    completions = {
        c.subject_id: c.completed
        for c in SessionCompletion.query.filter_by(session_date=today).all()
    }
    for session in timetable:
        session["completed"] = completions.get(session["id"], False)

    return jsonify({"timetable": timetable, "daily_minutes": daily_minutes}), 200


@main_bp.route("/api/weekly-plan", methods=["GET"])
def get_weekly_plan():
    return jsonify({"weekly_plan": generate_weekly_plan()}), 200


# --- Progress tracking ---

@main_bp.route("/api/sessions/<int:subject_id>/complete", methods=["POST"])
def toggle_session_completion(subject_id):
    subject = db.session.get(Subject, subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    today = date.today()
    completion = SessionCompletion.query.filter_by(
        subject_id=subject_id, session_date=today
    ).first()

    if not completion:
        completion = SessionCompletion(subject_id=subject_id, session_date=today, completed=True)
        db.session.add(completion)
    else:
        completion.completed = not completion.completed

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Failed to update session"}), 500

    return jsonify({"subject_id": subject_id, "completed": completion.completed}), 200


# --- Dashboard & exams ---

@main_bp.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    daily_minutes = _get_daily_budget_minutes()
    today = date.today()
    subjects = Subject.query.all()
    timetable = generate_timetable(daily_budget_minutes=daily_minutes)

    completed_today = SessionCompletion.query.filter_by(
        session_date=today, completed=True
    ).count()

    return jsonify({
        "total_subjects": len(subjects),
        "total_daily_minutes": sum(s["allocated_minutes"] for s in timetable),
        "upcoming_exams": sum(1 for s in subjects if (s.exam_date - today).days >= 0),
        "sessions_today": len(timetable),
        "completed_today": completed_today
    }), 200


@main_bp.route("/api/exams/upcoming", methods=["GET"])
def get_upcoming_exams():
    today = date.today()
    subjects = Subject.query.filter(Subject.exam_date >= today).order_by(
        Subject.exam_date.asc()
    ).all()

    exams = [{
        "id": s.id,
        "name": s.name,
        "exam_date": s.exam_date.isoformat(),
        "days_left": (s.exam_date - today).days
    } for s in subjects]

    return jsonify({"exams": exams}), 200


# --- Global error handlers ---

@main_bp.app_errorhandler(404)
def handle_404(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Endpoint not found"}), 404
    return render_template("index.html"), 404


@main_bp.app_errorhandler(405)
def handle_405(e):
    return jsonify({"error": "Method not allowed on this endpoint"}), 405


@main_bp.app_errorhandler(500)
def handle_500(e):
    db.session.rollback()
    return jsonify({"error": "Internal server error. Please try again."}), 500
