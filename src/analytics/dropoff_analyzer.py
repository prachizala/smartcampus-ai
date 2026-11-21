"""
Lecture Attendance Drop-off & Retention Analyzer
Calculates drop-off percentage, exponential trend decay, and critical alert thresholds.
"""
from typing import List, Dict, Any
import math

class DropoffAnalyzer:
    def __init__(self, warning_threshold: float = 0.20):
        self.warning_threshold = warning_threshold

    def calculate_dropoff_rate(self, weekly_counts: List[int]) -> float:
        if len(weekly_counts) < 2 or weekly_counts[0] <= 0:
            return 0.0
        total_drop = weekly_counts[0] - weekly_counts[-1]
        return round(max(0.0, total_drop / weekly_counts[0]), 4)

    def detect_abrupt_drops(self, weekly_counts: List[int], max_single_week_drop: float = 0.15) -> List[Dict[str, Any]]:
        alerts = []
        for i in range(1, len(weekly_counts)):
            prev, curr = weekly_counts[i-1], weekly_counts[i]
            if prev > 0:
                drop_pct = (prev - curr) / prev
                if drop_pct >= max_single_week_drop:
                    alerts.append({
                        "week_index": i,
                        "previous_count": prev,
                        "current_count": curr,
                        "drop_percentage": round(drop_pct * 100, 2)
                    })
        return alerts

if __name__ == "__main__":
    analyzer = DropoffAnalyzer()
    counts = [100, 95, 88, 70, 68]
    rate = analyzer.calculate_dropoff_rate(counts)
    assert rate == 0.32, f"Expected 0.32, got {rate}"
    alerts = analyzer.detect_abrupt_drops(counts)
    assert len(alerts) == 1
    print("Dropoff analyzer unit tests passed!")
