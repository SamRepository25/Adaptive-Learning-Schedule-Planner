from datetime import datetime

from flask import Blueprint, render_template, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import Subject
from app.scheduler import generate_schedule

main_bp = Blueprint("main", __name__)

VALID_DIFFICULTIES = (1, 3, 5)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/api/subjects", methods=["GET"])
def get_subjects():
    subjects = Subject.query.order_by(Subject.exam_date.asc()).all()
    return jsonify([s.to_dict() for s in subjects]), 200


@main_bp.route("/api/subjects", methods=["POST"])
def add_subject():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    name = data.get("name", "").strip()
    exam_date_raw = data.get("exam_date", "").strip()
    difficulty = data.get("difficulty")

    # Validation
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
        return jsonify(
            {"error": "Difficulty must be 1 (Easy), 3 (Medium), or 5 (Hard)"}
        ), 400

    if Subject.query.filter_by(name=name).first():
        return jsonify({"error": f"Subject '{name}' already exists"}), 409

    subject = Subject(
        name=name,
        exam_date=exam_date,
        difficulty=difficulty
    )

    db.session.add(subject)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Failed to save subject. Please try again."}), 500

    return jsonify(subject.to_dict()), 201


@main_bp.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)

    if not subject:
        return jsonify({"error": f"Subject with id {subject_id} not found"}), 404

    db.session.delete(subject)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Failed to delete subject. Please try again."}), 500

    return jsonify({"message": f"Subject '{subject.name}' deleted"}), 200


@main_bp.route("/api/schedule", methods=["GET"])
def get_schedule():
    schedule = generate_schedule()

    if not schedule:
        return jsonify({
            "message": "No subjects added yet",
            "schedule": []
        }), 200

    return jsonify({"schedule": schedule}), 200


# -----------------------------
# Global Error Handlers
# -----------------------------

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