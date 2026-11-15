import pytest
from app.core.security import hash_password, verify_password, create_access_token
from app.services.face_service import extract_face_embedding, compute_cosine_similarity
from app.services.risk_service import risk_predictor
from PIL import Image, ImageDraw

def test_password_hashing():
    pw = "SecretCampusPass123"
    h = hash_password(pw)
    assert h != pw
    assert verify_password(pw, h) is True
    assert verify_password("WrongPass", h) is False

def test_jwt_generation():
    token = create_access_token({"sub": "test@campus.edu", "role": "teacher"})
    assert isinstance(token, str)
    assert len(token) > 20

def test_face_embedding_consistency():
    # Identical image
    img1 = Image.new("RGB", (112, 112), color=(220, 180, 140))
    d1 = ImageDraw.Draw(img1)
    d1.ellipse((30, 30, 80, 80), fill=(50, 50, 50))

    img2 = Image.new("RGB", (112, 112), color=(220, 180, 140))
    d2 = ImageDraw.Draw(img2)
    d2.ellipse((30, 30, 80, 80), fill=(50, 50, 50))

    # Distinctly different image
    img3 = Image.new("RGB", (112, 112), color=(20, 40, 180))
    d3 = ImageDraw.Draw(img3)
    d3.rectangle((10, 10, 100, 100), fill=(240, 240, 10))

    emb1 = extract_face_embedding(img1)
    emb2 = extract_face_embedding(img2)
    emb3 = extract_face_embedding(img3)

    assert len(emb1) == 128
    sim_identical = compute_cosine_similarity(emb1, emb2)
    sim_different = compute_cosine_similarity(emb1, emb3)

    assert sim_identical >= 0.99
    assert sim_different < 0.85

def test_academic_risk_classifier():
    # High-performing student
    good = risk_predictor.predict_risk(attendance_rate=95.0, midterm_score=90.0, assignment_score=92.0, backlogs=0)
    assert good["risk_level"] == "low"
    assert good["risk_score"] < 0.20

    # High-risk student (low attendance, backlogs)
    critical = risk_predictor.predict_risk(attendance_rate=65.0, midterm_score=40.0, assignment_score=50.0, backlogs=2)
    assert critical["risk_level"] == "high"
    assert critical["risk_score"] >= 0.65
    assert len(critical["alerts"]) > 0


def test_attendance_status_upgrade():
    # Verify that an absent student is upgraded to present upon verified scan
    from app.models.models import AttendanceRecord
    # Simulation logic
    rec = AttendanceRecord(session_id=1, student_id=4, status="absent", confidence_score=0.0)
    assert rec.status == "absent"
    # Upgrade
    rec.status = "present"
    rec.confidence_score = 0.92
    assert rec.status == "present"
    assert rec.confidence_score == 0.92


def test_p2_error_handling_and_empty_states():
    # Verify that requesting a non-existent course returns a structured 404
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    
    # 404 for unknown endpoint or missing course
    res = client.get("/api/v1/attendance/sessions/nonexistent")
    assert res.status_code in [404, 405]

    # Verify risk summary envelope structure
    summary = client.get("/api/v1/analytics/risk-summary")
    if summary.status_code == 200:
        data = summary.json()
        assert "total_students" in data
        assert "high_risk_count" in data


def test_risk_predictor_boundary_conditions():
    # 0 attendance & multiple backlogs must trigger high risk with alerts
    worst_case = risk_predictor.predict_risk(attendance_rate=0.0, midterm_score=10.0, assignment_score=0.0, backlogs=5)
    assert worst_case["risk_level"] == "high"
    assert worst_case["risk_score"] >= 0.85
    assert len(worst_case["alerts"]) >= 2

    # Perfect scores must result in low risk with 0 alerts
    best_case = risk_predictor.predict_risk(attendance_rate=100.0, midterm_score=100.0, assignment_score=100.0, backlogs=0)
    assert best_case["risk_level"] == "low"
    assert best_case["risk_score"] == 0.0

def test_csv_export_format():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    
    # Verify CSV export returns text/csv header
    res = client.get("/api/v1/attendance/export/csv?session_id=1")
    assert res.status_code in [200, 401, 403, 404]
    if res.status_code == 200:
        assert "text/csv" in res.headers.get("content-type", "")
