"""
Campus Computing Lab Resource Optimizer
Matches student laboratory sections with optimal lab seat configurations.
"""
from typing import List, Dict, Any

class LabResourceOptimizer:
    def __init__(self, lab_capacities: Dict[str, int]):
        self.labs = lab_capacities

    def allocate_optimal_lab(self, cohort_size: int) -> Dict[str, Any]:
        eligible = {k: v for k, v in self.labs.items() if v >= cohort_size}
        if not eligible:
            return {"allocated_lab": None, "waste_seats": 0, "status": "INSUFFICIENT_CAPACITY"}
        best_lab = min(eligible, key=eligible.get)
        waste = self.labs[best_lab] - cohort_size
        return {
            "allocated_lab": best_lab,
            "capacity": self.labs[best_lab],
            "cohort_size": cohort_size,
            "waste_seats": waste,
            "status": "ALLOCATED"
        }

if __name__ == "__main__":
    opt = LabResourceOptimizer({"LAB_A": 30, "LAB_B": 60, "LAB_C": 120})
    res = opt.allocate_optimal_lab(45)
    assert res["allocated_lab"] == "LAB_B"
    assert res["waste_seats"] == 15
    print("Lab resource optimizer unit tests passed!")
