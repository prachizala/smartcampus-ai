from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, StudentPerformance, AttendanceRecord, Session as ClassSession
from app.services.risk_service import risk_predictor

router = APIRouter()

@router.get("/risk-summary")
def get_risk_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profiles = db.query(StudentPerformance).all()
    total = len(profiles)
    high_risk = []
    med_risk = []
    low_risk = []

    for p in profiles:
        student_name = p.student.full_name if p.student else f"Student #{p.student_id}"
        roll = p.student.student_id if p.student else f"STU-{p.student_id}"
        item = {
            "student_id": p.student_id,
            "full_name": student_name,
            "roll_number": roll,
            "attendance_rate": p.attendance_rate,
            "midterm_score": p.midterm_score,
            "assignment_score": p.assignment_score,
            "backlogs": p.backlogs,
            "risk_score": p.risk_score,
            "risk_level": p.risk_level
        }
        if p.risk_level == "high":
            high_risk.append(item)
        elif p.risk_level == "medium":
            med_risk.append(item)
        else:
            low_risk.append(item)

    return {
        "total_students": total,
        "high_risk_count": len(high_risk),
        "medium_risk_count": len(med_risk),
        "low_risk_count": len(low_risk),
        "critical_cutoff_pct": 75.0,
        "high_risk_students": high_risk,
        "medium_risk_students": med_risk
    }

@router.get("/attendance-trends")
def get_attendance_trends(db: Session = Depends(get_db)):
    sessions = db.query(ClassSession).order_by(ClassSession.id.asc()).limit(7).all()
    trend = []
    for s in sessions:
        present_count = len([r for r in s.attendance_records if r.status == "present"])
        total_enrolled = 10  # Standard cohort
        pct = round((present_count / max(1, total_enrolled)) * 100, 1)
        trend.append({
            "date": s.session_date,
            "topic": s.topic,
            "present_count": present_count,
            "attendance_pct": pct
        })
    return {"trend": trend}
