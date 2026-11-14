# Product Requirements Document (PRD)
## SmartCampus AI: AI Attendance & Academic Risk Predictor

### 1. Executive Summary & Problem Statement
Higher education institutions face two compounding operational challenges:
1. **Attendance Friction & Proxying**: Manual roll calls consume 10-15% of instructional lecture time and paper/RFID sign-ins are routinely exploited by peer proxying.
2. **Late-Stage Academic Attrition**: Academic failure and dropout risks are typically flagged only after semester end-term examinations, leaving mentors no proactive window for academic intervention.

**SmartCampus AI** delivers an integrated campus intelligence portal uniting lightweight biometric face-recognition attendance with a scikit-learn machine learning risk predictor. Faculty mark class attendance in seconds via webcam stream while real-time predictive analytics categorize student risk levels (High, Moderate, Low), enabling timely remedial intervention.

---

### 2. User Personas
- **Institutional Admin (Dean / Registrar)**: Manages university master records, faculty accounts, course mappings, and institutional compliance reports.
- **Faculty / Course Instructor**: Launches classroom attendance sessions via live webcam or snapshots, reviews class registers, overrides verified absences with medical audit logs, and monitors academic risk dashboards.
- **Student**: Reviews personal subject-wise attendance percentages, receives low-attendance warnings (< 75%), views risk alerts, and accesses customized academic recovery advice.

---

### 3. Scope & Prioritization (MoSCoW)
Scope is strictly frozen at the conclusion of Day 1.

#### MUST HAVE (Target MVP - Days 1-5)
- **Role-Based Access Control**: JWT authentication separating Admin, Teacher, and Student permissions with bcrypt password hashing.
- **Biometric Face Attendance Pipeline**: Enrollment of student facial embeddings (128-d / 512-d feature vectors); live webcam frame match with cosine similarity thresholding; instant duplicate prevention.
- **Attendance Ledger & Export**: Class session creation, automated status assignment (Present, Absent, Late), manual attendance override with audit logs, and CSV export.
- **Academic Risk Predictor**: Scikit-learn predictive classifier evaluating student historical attendance rate, continuous internal assessment (CIA) scores, assignment completion rate, and laboratory backlogs to output calibrated risk probabilities.
- **Interactive Analytics Dashboard**: Responsive charts (attendance trends over time, class risk distribution, at-risk student leaderboard) rendered via Recharts/Chart.js.
- **Automated Alerts**: Visual warning banners for attendance below 75% regulatory mandate or high predictive risk scores.

#### SHOULD HAVE (Days 5-6)
- Student self-service portal with personalized progress metrics.
- Multi-subject cumulative attendance heatmaps.
- Email/in-app notification triggers for automated warning dispatches.

#### COULD HAVE (Deferred to Post-MVP)
- Live RTSP IP camera continuous video stream parsing.
- Anti-spoofing liveness verification via eye-blink or head-pose detection.

#### WON'T HAVE (Out of Scope for 7-Day Sprint)
- Hardware turnstile integration.
- Native mobile applications (responsive mobile web supported).

---

### 4. Non-Functional Requirements
- **Performance**: Face recognition verification in under 500ms per face on CPU; API response time < 200ms for data endpoints.
- **Accuracy & Honesty**: All risk prediction accuracy metrics reported must reflect empirical evaluation on an isolated test dataset.
- **Privacy & Security**: Zero raw image files stored post-enrollment; only encrypted/normalized mathematical vector embeddings stored.
- **Usability**: Clean, modern, accessible UI built for fast classroom operation with zero complex setup.
