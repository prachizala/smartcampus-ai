import json
import numpy as np
from PIL import Image, ImageDraw
from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.models import User, Course, Session as ClassSession, AttendanceRecord, StudentPerformance
from app.services.face_service import extract_face_embedding
from app.services.risk_service import risk_predictor

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def generate_mock_face(name: str, color: tuple) -> str:
    img = Image.new("RGB", (112, 112), color=color)
    draw = ImageDraw.Draw(img)
    draw.ellipse((20, 20, 92, 92), fill=(255, 220, 190), outline=(100, 50, 20))
    # Draw simple facial features based on name hash
    h = hash(name) % 20
    draw.ellipse((38, 45, 48, 55), fill=(30, 30, 30))
    draw.ellipse((64, 45, 74, 55), fill=(30, 30, 30))
    draw.arc((40, 65, 72, 85 + h % 5), 0, 180, fill=(180, 40, 40), width=3)
    emb = extract_face_embedding(img)
    return json.dumps(emb)

print("Seeding SmartCampus AI database...")

# 1. Admin
if not db.query(User).filter(User.email == "admin@smartcampus.edu").first():
    admin = User(
        email="admin@smartcampus.edu",
        hashed_password=hash_password("admin123"),
        full_name="Dr. Alok Verma (Registrar)",
        role="admin"
    )
    db.add(admin)

# 2. Teacher
teacher = db.query(User).filter(User.email == "prof.sharma@smartcampus.edu").first()
if not teacher:
    teacher = User(
        email="prof.sharma@smartcampus.edu",
        hashed_password=hash_password("teacher123"),
        full_name="Prof. Sunita Sharma",
        role="teacher"
    )
    db.add(teacher)
    db.commit()

# 3. Courses
course = db.query(Course).filter(Course.course_code == "BCA301").first()
if not course:
    course = Course(
        course_code="BCA301",
        course_name="Data Structures & Algorithms",
        teacher_id=teacher.id
    )
    db.add(course)
    db.commit()

# 4. Students & Performance
students_data = [
    ("Prachi Zala", "BCA2401", "prachi@smartcampus.edu", (120, 180, 240), 94.0, 88.0, 92.0, 0),
    ("Aarav Patel", "BCA2402", "aarav@smartcampus.edu", (240, 150, 150), 91.0, 82.0, 85.0, 0),
    ("Rhea Sengupta", "BCA2403", "rhea@smartcampus.edu", (150, 220, 150), 85.0, 76.0, 79.0, 0),
    ("Kabir Mehta", "BCA2404", "kabir@smartcampus.edu", (240, 220, 130), 73.0, 58.0, 65.0, 1),
    ("Ishaan Joshi", "BCA2405", "ishaan@smartcampus.edu", (200, 160, 220), 68.0, 42.0, 50.0, 2),
    ("Tanvi Deshmukh", "BCA2406", "tanvi@smartcampus.edu", (180, 200, 220), 62.0, 39.0, 45.0, 3),
    ("Devansh Rao", "BCA2407", "devansh@smartcampus.edu", (220, 180, 160), 88.0, 84.0, 86.0, 0),
    ("Ananya Nair", "BCA2408", "ananya@smartcampus.edu", (190, 240, 200), 78.0, 69.0, 75.0, 0),
]

for name, roll, email, color, att, mid, ass, bkl in students_data:
    u = db.query(User).filter(User.email == email).first()
    if not u:
        u = User(
            email=email,
            hashed_password=hash_password("student123"),
            full_name=name,
            role="student",
            student_id=roll,
            face_embedding=generate_mock_face(name, color)
        )
        db.add(u)
        db.commit()

        # Risk prediction evaluation
        pred = risk_predictor.predict_risk(att, mid, ass, bkl)
        perf = StudentPerformance(
            student_id=u.id,
            attendance_rate=att,
            midterm_score=mid,
            assignment_score=ass,
            backlogs=bkl,
            risk_score=pred["risk_score"],
            risk_level=pred["risk_level"]
        )
        db.add(perf)
        db.commit()

# 5. Sessions & Records
session1 = db.query(ClassSession).filter(ClassSession.topic == "Binary Search Trees").first()
if not session1:
    session1 = ClassSession(course_id=course.id, session_date="2026-11-10", topic="Binary Search Trees")
    session2 = ClassSession(course_id=course.id, session_date="2026-11-12", topic="Graph Traversal (BFS/DFS)")
    session3 = ClassSession(course_id=course.id, session_date="2026-11-14", topic="Dynamic Programming")
    db.add_all([session1, session2, session3])
    db.commit()

    # Add sample attendance
    all_students = db.query(User).filter(User.role == "student").all()
    for s in all_students:
        status = "present" if s.risk_profile and s.risk_profile.attendance_rate > 70.0 else "absent"
        r1 = AttendanceRecord(session_id=session1.id, student_id=s.id, status=status, confidence_score=0.94)
        r2 = AttendanceRecord(session_id=session2.id, student_id=s.id, status=status, confidence_score=0.92)
        r3 = AttendanceRecord(session_id=session3.id, student_id=s.id, status="present", confidence_score=0.95)
        db.add_all([r1, r2, r3])
    db.commit()

print("SmartCampus AI database seeded successfully!")
