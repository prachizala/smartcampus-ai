"""Smart campus HVAC, ventilation, and lighting power consumption monitor."""


class CampusEnergyMonitor:
    """Evaluates kilowatt-hour power draw against ambient temperature baselines."""

    PEAK_RATE_THRESHOLD_KW = 120.0

    @classmethod
    def evaluate_consumption(cls, current_draw_kw: float, is_building_occupied: bool) -> dict:
        """Determines if building energy footprint is anomalous."""
        status = "NORMAL"
        if not is_building_occupied and current_draw_kw > 15.0:
            status = "PHANTOM_DRAIN_ALERT"
        elif current_draw_kw > cls.PEAK_RATE_THRESHOLD_KW:
            status = "PEAK_DEMAND_WARNING"

        return {
            "current_draw_kw": current_draw_kw,
            "is_occupied": is_building_occupied,
            "status": status,
        }
