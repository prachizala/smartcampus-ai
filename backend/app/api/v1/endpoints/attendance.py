import csv
import io
import json
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, RoleChecker
from app.models.models import User, Course, Session as ClassSession, AttendanceRecord, StudentPerformance
from app.services.face_service import decode_base64_image, extract_face_embedding, match_face_against_gallery

router = APIRouter()

class CreateSessionRequest(BaseModel):
    course_code: str
    session_date: str
    topic: str

class FaceVerifyRequest(BaseModel):
    session_id: int
    image_base64: str

@router.post("/sessions")
def create_session(
    req: CreateSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin", "teacher"]))
):
    course = db.query(Course).filter(Course.course_code == req.course_code).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with code '{req.course_code}' not found")

    new_session = ClassSession(
        course_id=course.id,
        session_date=req.session_date,
        topic=req.topic
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"session_id": new_session.id, "course_code": course.course_code, "topic": new_session.topic}

@router.get("/sessions")
def list_sessions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sessions = db.query(ClassSession).order_by(ClassSession.id.desc()).all()
    out = []
    for s in sessions:
        out.append({
            "id": s.id,
            "course_code": s.course.course_code if s.course else "GEN101",
            "course_name": s.course.course_name if s.course else "General Lecture",
            "session_date": s.session_date,
            "topic": s.topic,
            "attendance_count": len(s.attendance_records) if s.attendance_records else 0
        })
    return out

@router.post("/verify-face")
def verify_face_attendance(
    req: FaceVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(RoleChecker(["admin", "teacher"]))
):
    session_obj = db.query(ClassSession).filter(ClassSession.id == req.session_id).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    try:
        pil_img = decode_base64_image(req.image_base64)
        query_vector = extract_face_embedding(pil_img)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

    students = db.query(User).filter(User.role == "student", User.face_embedding.isnot(None)).all()
    gallery = []
    for s in students:
        try:
            emb = json.loads(s.face_embedding)
            gallery.append({
                "student_id": s.id,
                "full_name": s.full_name,
                "roll_number": s.student_id or f"STU-{s.id}",
                "embedding": emb
            })
        except Exception:
            continue

    match, confidence = match_face_against_gallery(query_vector, gallery, threshold=0.70)
    if not match:
        return {
            "matched": False,
            "confidence": confidence,
            "message": "Face not recognized. Student not enrolled or match confidence below threshold."
        }

    matched_user_id = match["student_id"]

    # Check for existing record in this session
    existing = db.query(AttendanceRecord).filter(
        AttendanceRecord.session_id == req.session_id,
        AttendanceRecord.student_id == matched_user_id
    ).first()

    if existing:
        # If previously marked absent, upgrade to present!
        if existing.status == "absent":
            existing.status = "present"
            existing.confidence_score = confidence
            existing.marked_at = datetime.utcnow()
            db.commit()
            return {
                "matched": True,
                "already_marked": False,
                "upgraded_from_absent": True,
                "student_name": match["full_name"],
                "roll_number": match["roll_number"],
                "confidence": confidence,
                "status": "present",
                "message": f"Status updated from Absent to Present for {match['full_name']}."
            }
        return {
            "matched": True,
            "already_marked": True,
            "student_name": match["full_name"],
            "roll_number": match["roll_number"],
            "confidence": confidence,
            "status": existing.status,
            "message": f"Attendance already recorded as {existing.status.upper()} for {match['full_name']}."
        }

    new_record = AttendanceRecord(
        session_id=req.session_id,
        student_id=matched_user_id,
        status="present",
        confidence_score=confidence
    )
    db.add(new_record)
    db.commit()

    return {
        "matched": True,
        "already_marked": False,
        "student_name": match["full_name"],
        "roll_number": match["roll_number"],
        "confidence": confidence,
        "status": "present",
        "message": f"Successfully verified & marked Present: {match['full_name']}"
    }

@router.get("/export/csv")
def export_attendance_csv(session_id: Optional[int] = None, db: Session = Depends(get_db)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Record ID", "Session ID", "Course", "Date", "Student Name", "Roll Number", "Status", "Confidence", "Timestamp"])

    query = db.query(AttendanceRecord)
    if session_id:
        query = query.filter(AttendanceRecord.session_id == session_id)
    records = query.all()

    for r in records:
        s_name = r.student.full_name if (r.student and r.student.full_name) else "Unknown"
        s_roll = r.student.student_id if (r.student and r.student.student_id) else "N/A"
        c_code = r.session.course.course_code if (r.session and r.session.course and r.session.course.course_code) else "GEN101"
        s_date = r.session.session_date if (r.session and r.session.session_date) else "Unknown"
        conf = f"{r.confidence_score*100:.1f}%" if r.confidence_score is not None else "100.0%"
        writer.writerow([r.id, r.session_id, c_code, s_date, s_name, s_roll, r.status, conf, r.marked_at])

    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=attendance_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"}
    )
