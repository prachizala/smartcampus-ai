# Design Specification
## SmartCampus AI: UI/UX & Component System

### 1. Visual Language & Aesthetics
SmartCampus AI utilizes an authoritative, modern academic dashboard aesthetic designed for high legibility in brightly lit classrooms and lecture halls.

- **Color Palette**:
  - **Slate Primary**: `#0f172a` (Sidebar, Headers, High-contrast text)
  - **Academic Indigo**: `#4338ca` (Active buttons, Focus rings, Brand accents)
  - **Emerald Success**: `#10b981` (Present status, Low risk indicator)
  - **Amber Caution**: `#f59e0b` (Moderate risk, Late attendance)
  - **Rose Critical**: `#f43f5e` (High academic risk, Absent status, Attendance < 75%)
  - **Canvas Neutral**: `#f8fafc` (Background canvas)
- **Typography**: Inter / system font stack. Tabular numbers enabled for data grids (`font-feature-settings: 'tnum'`).

---

### 2. Core Layouts & Screen Flow
1. **Login Screen**: Minimalist card with quick demo login presets (`Demo Admin`, `Demo Teacher`, `Demo Student`).
2. **Teacher Command Center**:
   - Top Bar: Selected Course Selector, Today's Date, Quick Action Buttons.
   - Left Column (40% width): Live Attendance Scanner with webcam viewport, face bounding overlay, live status ticker ("Prachi Zala verified - 98%").
   - Right Column (60% width): Real-time Attendance Roster grid with manual toggle switches (Present, Late, Absent).
3. **Academic Risk & Early Warning Screen**:
   - KPI Banner: Average Attendance (%), Students at High Risk, Attrition Vulnerability index.
   - Distribution Chart: Bar chart of attendance distribution vs test scores.
   - Actionable Risk Table: Student profile, predicted risk score, primary risk factors, and 'Generate Intervention Slip' trigger.
4. **Student Self-Service View**:
   - Visual progress ring showing overall attendance vs 75% regulatory cutoff.
   - Warning modal: "Attention: Your attendance in CS301 is 71%. Attend next 3 lectures to exit probation."
