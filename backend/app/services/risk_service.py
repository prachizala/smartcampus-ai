import numpy as np
from typing import Dict, Any, List

class AcademicRiskPredictor:
    """
    Transparent Machine Learning Academic Risk Classifier.
    Evaluates:
      1. Attendance Deficiency (Weight: 45%)
      2. Midterm Assessment Deficiency (Weight: 25%)
      3. Assignment Non-completion (Weight: 15%)
      4. Academic Backlogs Penalty (Weight: 15 points per backlog)
    """
    def __init__(self):
        self.w_att = 0.45
        self.w_mid = 0.25
        self.w_ass = 0.15
        self.w_bkl = 15.0

    def predict_risk(
        self,
        attendance_rate: float,
        midterm_score: float,
        assignment_score: float,
        backlogs: int
    ) -> Dict[str, Any]:
        # Calculate deficiencies (0 to 100 scale)
        att_def = max(0.0, 100.0 - float(attendance_rate))
        mid_def = max(0.0, 100.0 - float(midterm_score))
        ass_def = max(0.0, 100.0 - float(assignment_score))
        bkl_pen = min(30.0, float(backlogs) * self.w_bkl)

        total_penalty = (att_def * self.w_att) + (mid_def * self.w_mid) + (ass_def * self.w_ass) + bkl_pen
        risk_score = round(min(1.0, max(0.0, total_penalty / 100.0)), 3)

        # Classify risk level
        if risk_score >= 0.65 or attendance_rate < 75.0 or backlogs >= 2:
            level = "high"
            status_desc = "Immediate academic intervention required"
            alerts = ["Mandatory remedial mentoring", "Parental notification trigger"]
        elif risk_score >= 0.35 or attendance_rate < 80.0 or backlogs == 1:
            level = "medium"
            status_desc = "Moderate risk — monitored study group suggested"
            alerts = ["Course advisor check-in recommended"]
        else:
            level = "low"
            status_desc = "On track for academic honors"
            alerts = []

        recommendations = []
        if attendance_rate < 75.0:
            recommendations.append(f"Attendance is {attendance_rate}%. Target 85% to avoid exam debarment.")
        if midterm_score < 50.0:
            recommendations.append(f"Midterm score is {midterm_score}%. Join weekly tutorial sessions.")
        if backlogs > 0:
            recommendations.append(f"{backlogs} active backlog(s). Enroll in fast-track credit recovery.")
        if not recommendations:
            recommendations.append("Performance is excellent. Continue current study schedule.")

        return {
            "risk_score": risk_score,
            "risk_level": level,
            "status_description": status_desc,
            "alerts": alerts,
            "recommendations": recommendations,
            "attendance_rate": attendance_rate,
            "midterm_score": midterm_score,
            "assignment_score": assignment_score,
            "backlogs": backlogs
        }

risk_predictor = AcademicRiskPredictor()
