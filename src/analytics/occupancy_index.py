"""Classroom spatial occupancy density and capacity utilization monitor."""


class ClassroomOccupancyMonitor:
    """Evaluates lecture hall utilization and social distancing density indexes."""

    @staticmethod
    def calculate_utilization(occupied_seats: int, total_capacity: int) -> dict:
        """Returns utilization percentage and capacity alert status."""
        if total_capacity <= 0:
            return {"utilization_pct": 0.0, "status": "UNKNOWN"}

        utilization = (occupied_seats / total_capacity) * 100.0
        status = "CRITICAL_OVERCROWDED" if utilization > 90.0 else ("OPTIMAL" if utilization >= 50.0 else "UNDERUTILIZED")

        return {
            "occupied_seats": occupied_seats,
            "total_capacity": total_capacity,
            "utilization_pct": round(utilization, 2),
            "status": status,
        }
