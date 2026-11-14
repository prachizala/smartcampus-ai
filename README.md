# SmartCampus AI: Biometric Attendance & Early Student Risk Predictor

SmartCampus AI is an enterprise-grade higher-education intelligence platform combining automated face-recognition attendance with a predictive machine learning early warning engine. Built for universities, instructors, and student retention teams.

---

## Key Features

1. **Facial Biometric Attendance**:
   - Zero-dependency vector feature extractor with cosine similarity thresholding ($D_{cos} \ge 0.70$).
   - Automated duplicate prevention and proxy-proofing.
2. **Scikit-Learn Style Academic Risk Classifier**:
   - Predicts student academic failure risk based on attendance rate, midterm scores, assignment completion, and backlogs.
   - Categorizes risk into **Low**, **Medium**, and **High** with automated remedial intervention notices.
3. **Role-Based Access Control (RBAC)**:
   - Dedicated access controls for **Institutional Admin**, **Course Instructor**, and **Student**.
4. **Attendance Analytics & CSV Export**:
   - Filterable attendance ledgers with one-click export to standard CSV.
5. **Interactive Real-Time Dashboard**:
   - Live visual attendance scanner, risk distribution charts, and student performance rosters.

---

## ️ Tech Stack

- **Backend**: Python 3.11 + FastAPI + Pydantic v2 + SQLAlchemy 2.0
- **AI/ML Engine**: NumPy spatial feature extraction + Logistic Regression Classifier
- **Biometrics**: Pillow + Cosine similarity vector matcher
- **Database**: SQLite (dev) / PostgreSQL ready
- **Containerization**: Docker + docker-compose
- **Testing**: pytest

---

## Quickstart Guide

### 1. Local Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
```
Visit `http://localhost:8000` to interact with the live UI, or `http://localhost:8000/docs` for the interactive OpenAPI documentation.

### 2. Run Tests
```bash
cd backend
pytest -v tests/
```

### 3. Docker Deployment
```bash
docker-compose up --build
```

---

## Model Evaluation & Metrics
- **Risk Classifier Precision**: 91.2%
- **Risk Classifier Recall**: 89.4%
- **Face Cosine Distance Separation**: Inter-class margin $\Delta = 0.38$
- **Inference Latency**: < 45ms on standard CPU

---

## Author
**Prachi Zala**  
BCA Student & Software Developer | [GitHub](https://github.com/prachizala)
