from datetime import datetime
from app import db


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    exam_date = db.Column(db.Date, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)  # 1=Easy, 3=Medium, 5=Hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "exam_date": self.exam_date.isoformat(),
            "difficulty": self.difficulty,
            "created_at": self.created_at.isoformat()
        }


class SessionCompletion(db.Model):
    __tablename__ = "session_completions"

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("subject_id", "session_date", name="uq_subject_session_date"),
    )
