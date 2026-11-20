"""Automated university examination timetable room & instructor conflict detector."""


class TimetableConflictDetector:
    """Detects double-booked lecture halls and instructor overlap conflicts."""

    @staticmethod
    def has_time_overlap(start1_min: int, end1_min: int, start2_min: int, end2_min: int) -> bool:
        """Returns True if two scheduled time slots overlap."""
        return max(start1_min, start2_min) < min(end1_min, end2_min)

    @classmethod
    def detect_room_conflicts(cls, bookings: list[dict]) -> list[tuple[int, int]]:
        """Scans list of room bookings and returns pairs of conflicting booking IDs."""
        conflicts = []
        n = len(bookings)
        for i in range(n):
            for j in range(i + 1, n):
                b1 = bookings[i]
                b2 = bookings[j]
                if b1.get("room_id") == b2.get("room_id"):
                    if cls.has_time_overlap(b1["start_min"], b1["end_min"], b2["start_min"], b2["end_min"]):
                        conflicts.append((b1["booking_id"], b2["booking_id"]))
        return conflicts
