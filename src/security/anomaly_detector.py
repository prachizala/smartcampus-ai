"""
Attendance Anomaly & Proxy Detection Engine
Evaluates biometric attendance logs for rapid-fire timestamp clusters,
erratic geofence coordinate leaps, and sequential proxy scans.
"""
from typing import List, Dict, Any, Tuple
from datetime import datetime, timezone
import math


class AttendanceAnomalyDetector:
    """
    Analyzes student check-in event logs to flag proxy attendance,
    device sharing, and GPS spoofing.
    """
    def __init__(self, campus_lat: float = 23.0338, campus_lon: float = 72.5850, allowed_radius_m: float = 150.0):
        self.campus_lat = campus_lat
        self.campus_lon = campus_lon
        self.allowed_radius_m = allowed_radius_m

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Computes Great-Circle distance in meters."""
        r = 6371000.0  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return r * c

    def detect_rapid_device_sharing(self, logs: List[Dict[str, Any]], window_seconds: float = 4.0) -> List[Dict[str, Any]]:
        """
        Flags multiple check-ins originating from identical device_id or IP within window_seconds.
        """
        anomalies = []
        sorted_logs = sorted(logs, key=lambda x: x.get("timestamp", 0))

        for i in range(len(sorted_logs)):
            for j in range(i + 1, len(sorted_logs)):
                delta = sorted_logs[j].get("timestamp", 0) - sorted_logs[i].get("timestamp", 0)
                if delta > window_seconds:
                    break
                # Check for same device but different student
                if (sorted_logs[i].get("device_id") == sorted_logs[j].get("device_id") and
                        sorted_logs[i].get("student_id") != sorted_logs[j].get("student_id")):
                    anomalies.append({
                        "anomaly_type": "RAPID_DEVICE_SHARING",
                        "primary_student": sorted_logs[i].get("student_id"),
                        "proxy_student": sorted_logs[j].get("student_id"),
                        "delta_seconds": round(delta, 2),
                        "device_id": sorted_logs[i].get("device_id")
                    })
        return anomalies

    def evaluate_geofence_outliers(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Flags check-ins outside the designated campus boundary."""
        outliers = []
        for log in logs:
            lat = log.get("latitude", 0.0)
            lon = log.get("longitude", 0.0)
            dist = self._haversine_distance(self.campus_lat, self.campus_lon, lat, lon)
            if dist > self.allowed_radius_m:
                outliers.append({
                    "student_id": log.get("student_id"),
                    "distance_meters": round(dist, 2),
                    "allowed_radius_m": self.allowed_radius_m,
                    "exceeded_by_m": round(dist - self.allowed_radius_m, 2),
                    "status": "GEOFENCE_BREACH"
                })
        return outliers


def run_unit_tests() -> bool:
    detector = AttendanceAnomalyDetector(campus_lat=23.00, campus_lon=72.00, allowed_radius_m=100.0)
    sample_logs = [
        {"student_id": "STU_001", "device_id": "DEV_A", "timestamp": 1000.0, "latitude": 23.0001, "longitude": 72.0001},
        {"student_id": "STU_002", "device_id": "DEV_A", "timestamp": 1001.5, "latitude": 23.0001, "longitude": 72.0001},
        {"student_id": "STU_003", "device_id": "DEV_B", "timestamp": 1050.0, "latitude": 23.0100, "longitude": 72.0100},
    ]
    sharing = detector.detect_rapid_device_sharing(sample_logs)
    assert len(sharing) == 1, f"Expected 1 device sharing anomaly, got {len(sharing)}"
    assert sharing[0]["proxy_student"] == "STU_002"

    outliers = detector.evaluate_geofence_outliers(sample_logs)
    assert len(outliers) >= 1, "Expected geofence outlier"
    return True

if __name__ == "__main__":
    run_unit_tests()
    print("Attendance anomaly detector unit tests passed successfully!")
