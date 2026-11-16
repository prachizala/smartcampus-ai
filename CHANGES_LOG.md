# Changes Log - SmartCampus AI

## Work Package 5: Boilerplate Repos and Profile Review

### Summary of Changes
1. **README.md Overhaul**:
   - Upgraded documentation with enterprise architecture, badges, and project overview.
   - Added in-depth **Facility Management & Classroom Scheduling** overview detailing automated HVAC/lighting controls, kilowatt-hour footprint monitoring, dynamic space re-allocation, and schedule conflict prevention.
   - Added comprehensive **IoT Telemetry Sensor Mock Schema** complete with full JSON Schema specification and realistic sample payload covering energy consumption (kWh), room occupancy, ambient temperature (°C), humidity, and CO2 ppm.
   - Documented core platform features: facial biometric attendance with cosine similarity ($D_{cos} \ge 0.70$), scikit-learn style academic risk classifier, role-based access control, CSV export, and React dashboard.
   - Added complete API Endpoints table and reproducible `curl` examples.
   - Added local run guide for both backend FastAPI and frontend React/Vite.
2. **CI & Pytest Configuration**:
   - Added `pytest.ini` with `pythonpath = backend` for seamless root-level pytest execution.
   - Enhanced `.github/workflows/ci.yml` to trigger on `push` (including `review-fixes`) and `pull_request` for both backend pytest testing and frontend bundle verification.
3. **Verification & Tests**:
   - Ran `pytest backend/tests/test_all.py` locally: 8 passed out of 8 tests.

### Items Skipped & Rationale
- **Physical Hardware Integration**: Skipped physical sensor hardware connectivity since this repository is structured as a software platform prototype with mock schemas and API controllers.

### Manual Steps Needed
- None for local execution. For real-world IoT deployment, deploy an MQTT broker (e.g., Mosquitto) or HTTP gateway to ingest physical sensor streams into the telemetry schema.
