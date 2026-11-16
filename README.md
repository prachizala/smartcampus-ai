# SmartCampus AI: Higher-Ed Biometrics, Facility Intelligence & Academic Risk Predictor

[![SmartCampus AI CI](https://github.com/prachizala/smartcampus-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/prachizala/smartcampus-ai/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SmartCampus AI is an enterprise-grade higher-education intelligence platform combining automated face-recognition attendance, student retention early-warning modeling, facility management, and IoT-driven classroom scheduling. Built for university administrations, academic deans, and campus facility directors.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Facility Management & Classroom Scheduling](#facility-management--classroom-scheduling)
- [IoT Telemetry Sensor Mock Schema](#iot-telemetry-sensor-mock-schema)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [API Endpoints Table & curl Samples](#api-endpoints-table--curl-samples)
- [Local Setup & Run Guide](#local-setup--run-guide)
- [Testing](#testing)
- [Continuous Integration](#continuous-integration)
- [Author & License](#author--license)

---

## Project Overview

Modern campuses struggle to bridge the gap between academic operations and physical infrastructure management. Student absenteeism and academic distress frequently go unnoticed until midterms, while lecture halls and labs run high-power HVAC and lighting systems when virtually empty. 

SmartCampus AI integrates academic telemetry (biometric attendance, assignment submissions, midterm scores) with physical space intelligence (room occupancy, power consumption, temperature) to create a cohesive campus operating system.

---

## Facility Management & Classroom Scheduling

### 1. Smart Facility Management
- **Automated HVAC & Lighting Controls**: Real-time room occupancy thresholds trigger automated adjustments to thermal comfort setpoints, curtailing energy waste in unoccupied lecture halls.
- **Energy Footprint Tracking**: Continuous aggregation of kilowatt-hour (kWh) power draw per classroom, laboratory, and department block.
- **Peak Load Shifting**: Identifies energy-intensive lab slots and recommends schedule adjustments to reduce utility demand charges.

### 2. Intelligent Classroom Scheduling
- **Dynamic Space Re-Allocation**: Compares enrolled student rosters and actual real-time attendance against physical room capacity, flagging underutilized or overcrowded auditoriums.
- **Conflict Prevention**: Validates temporal overlaps and room resource requirements (e.g., projectors, lab equipment, spatial seating) prior to schedule assignment.
- **Campus Heatmap**: Feeds live occupancy metrics to administration dashboards for campus-wide footfall visualization.

---

## IoT Telemetry Sensor Mock Schema

To facilitate integration with campus edge devices (ESP32 microcontrollers, Zigbee/LoRaWAN gateways, and occupancy cameras), SmartCampus AI specifies a standardized JSON telemetry payload:

### Telemetry JSON Schema
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CampusIoTSensorTelemetry",
  "type": "object",
  "properties": {
    "sensor_id": { "type": "string", "example": "SENSOR-BLK-C-L204" },
    "building_id": { "type": "string", "example": "ENGINEERING_BLOCK_C" },
    "room_id": { "type": "string", "example": "LH-204" },
    "timestamp": { "type": "string", "format": "date-time" },
    "metrics": {
      "type": "object",
      "properties": {
        "room_occupancy": { "type": "integer", "minimum": 0, "description": "Current head-count" },
        "room_capacity": { "type": "integer", "minimum": 1, "description": "Maximum seating capacity" },
        "energy_consumption_kwh": { "type": "number", "minimum": 0.0, "description": "Instantaneous power usage rate" },
        "temperature_celsius": { "type": "number", "description": "Ambient room temperature" },
        "humidity_percentage": { "type": "number", "minimum": 0.0, "maximum": 100.0 },
        "co2_ppm": { "type": "integer", "minimum": 300, "description": "Indoor air quality indicator" }
      },
      "required": ["room_occupancy", "energy_consumption_kwh", "temperature_celsius"]
    },
    "status": { "type": "string", "enum": ["ACTIVE", "IDLE", "MAINTENANCE"] }
  },
  "required": ["sensor_id", "building_id", "room_id", "timestamp", "metrics"]
}
```

### Sample Telemetry Event
```json
{
  "sensor_id": "IOT-ENG-204-ENV",
  "building_id": "ENG_BLOCK_B",
  "room_id": "LH-204",
  "timestamp": "2026-11-16T10:15:00Z",
  "metrics": {
    "room_occupancy": 48,
    "room_capacity": 60,
    "energy_consumption_kwh": 3.85,
    "temperature_celsius": 22.4,
    "humidity_percentage": 45.2,
    "co2_ppm": 680
  },
  "status": "ACTIVE"
}
```

---

## Core Features

1. **Facial Biometric Attendance**:
   - Zero-dependency vector feature extractor with cosine similarity thresholding ($D_{cos} \ge 0.70$).
   - Automated duplicate entry prevention and tamper-evident verification logs.
2. **Scikit-Learn Style Academic Risk Classifier**:
   - Logistic regression model that evaluates attendance percentage, midterm marks, assignment submission velocity, and backlogs.
   - Categorizes risk into **Low**, **Medium**, and **High**, outputting actionable remedial intervention guidance.
3. **Role-Based Access Control (RBAC)**:
   - Partitioned permissions across **Institutional Admin**, **Course Instructor**, and **Student**.
4. **Attendance Analytics & CSV Export**:
   - Filterable lecture attendance ledgers with one-click export to standard CSV format.
5. **Interactive Dashboard**:
   - React 18 + Vite frontend with live visual scanner, risk distribution charts, and student performance rosters.

---

## System Architecture

```
smartcampus-ai/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI for backend tests & frontend build
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # Modular route controllers
│   │   │   ├── analytics.py     # Academic risk & attendance trends
│   │   │   ├── attendance.py    # Session creation, face verify, CSV export
│   │   │   └── auth.py          # JWT authentication, registration & profile
│   │   ├── core/                # Configuration, security, and DB session
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── services/            # Biometric vector matcher & ML risk model
│   │   ├── static/              # Lightweight web interface
│   │   └── main.py              # FastAPI application entrypoint
│   ├── tests/
│   │   └── test_all.py          # Pytest test suite (auth, risk, biometrics)
│   ├── requirements.txt         # Production dependencies
│   └── seed_data.py             # Realistic campus demonstration dataset
├── frontend/                    # React 18 + Vite dashboard interface
├── pytest.ini                   # Pytest configuration
├── CHANGES_LOG.md               # Version & change audit trail
└── README.md                    # Enterprise documentation
```

---

## API Endpoints Table & curl Samples

Base URL: `http://localhost:8000`

| Method | Endpoint | Description | Auth Required |
|:---|:---|:---|:---:|
| `GET` | `/api/health` | Service health status and version metadata | No |
| `POST` | `/api/v1/seed` | Seed realistic demo students, courses & sessions | No |
| `POST` | `/api/v1/auth/register` | Register a new user (Admin / Instructor / Student) | No |
| `POST` | `/api/v1/auth/login` | Authenticate and obtain JWT bearer token | No |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user profile | Bearer Token |
| `POST` | `/api/v1/attendance/sessions` | Create a new class attendance session | Instructor / Admin |
| `GET` | `/api/v1/attendance/sessions` | List all active and past attendance sessions | Bearer Token |
| `POST` | `/api/v1/attendance/verify-face` | Verify face biometric embedding & mark attendance | Bearer Token |
| `GET` | `/api/v1/attendance/export/csv` | Export session attendance records as CSV | No |
| `GET` | `/api/v1/analytics/risk-summary` | Aggregate student academic failure risk counts | Bearer Token |
| `GET` | `/api/v1/analytics/attendance-trends` | Compute campus-wide attendance percentage trends | No |

### Sample `curl` Commands

#### 1. System Health Check
```bash
curl -X GET "http://localhost:8000/api/health"
```
*Response:*
```json
{"status": "healthy", "service": "SmartCampus AI", "version": "1.0.0"}
```

#### 2. Seed Demonstration Data
```bash
curl -X POST "http://localhost:8000/api/v1/seed"
```

#### 3. Instructor Authentication
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=instructor1&password=password123"
```
*Response:*
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "token_type": "bearer",
  "role": "INSTRUCTOR",
  "full_name": "Dr. Sarah Jenkins"
}
```

#### 4. Export Attendance to CSV
```bash
curl -X GET "http://localhost:8000/api/v1/attendance/export/csv?session_id=1" \
  --output attendance_session_1.csv
```

#### 5. Fetch Academic Risk Summary
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/risk-summary" \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>"
```

---

## Local Setup & Run Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend dashboard)
- Git

### 1. Backend Setup
```bash
cd smartcampus-ai
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# Populate realistic campus seed data
python backend/seed_data.py

# Launch FastAPI backend
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
- **API Documentation (Swagger):** `http://localhost:8000/docs`
- **ReDoc Documentation:** `http://localhost:8000/redoc`

### 2. Frontend Setup (Optional)
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` to view the interactive React dashboard.

---

## Testing

Run the automated backend test suite covering authentication, JWT token validation, facial vector consistency, academic risk bounds, and CSV exports:

From repository root:
```bash
pytest backend/tests/test_all.py -v
```
Or via python module runner:
```bash
python -m pytest backend/tests/test_all.py -v
```

---

## Continuous Integration

The repository includes a GitHub Actions CI workflow in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) that executes on every push and pull request:
- **Backend Job**: Sets up Python 3.11, installs requirements, and runs `pytest backend/tests/test_all.py`.
- **Frontend Job**: Sets up Node.js 20, installs npm dependencies, and verifies the production bundle build (`npm run build`).

---

## Author & License

- **Author:** Prachi Zala ([prachizala](https://github.com/prachizala))
- **Email:** prachizala2003@gmail.com
- **License:** MIT License. See [LICENSE](LICENSE) for details.
