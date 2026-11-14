from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="student")  # 'admin', 'teacher', 'student'
    student_id = Column(String, unique=True, index=True, nullable=True)
    face_embedding = Column(Text, nullable=True)  # JSON serialized vector
    created_at = Column(DateTime, default=datetime.utcnow)

    attendance_records = relationship("AttendanceRecord", back_populates="student")
    risk_profile = relationship("StudentPerformance", back_populates="student", uselist=False)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String, unique=True, index=True, nullable=False)
    course_name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("Session", back_populates="course")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    session_date = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="sessions")
    attendance_records = relationship("AttendanceRecord", back_populates="session")

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="present")  # 'present', 'late', 'absent'
    confidence_score = Column(Float, default=1.0)
    marked_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="attendance_records")
    student = relationship("User", back_populates="attendance_records")

class StudentPerformance(Base):
    __tablename__ = "student_performance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    attendance_rate = Column(Float, default=100.0)
    midterm_score = Column(Float, default=80.0)
    assignment_score = Column(Float, default=85.0)
    backlogs = Column(Integer, default=0)
    risk_score = Column(Float, default=0.1)
    risk_level = Column(String, default="low")  # 'low', 'medium', 'high'
    evaluated_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", back_populates="risk_profile")
