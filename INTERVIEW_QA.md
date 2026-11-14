# Technical Interview Questions & Answers — SmartCampus AI

Based on the actual codebase in `smartcampus-ai`.

---

### Question 1: How does the facial feature extraction and cosine similarity matching work in `face_service.py`?
**Answer:**
When an image is submitted (e.g., from the webcam feed via base64 encoding), the pipeline in `app/services/face_service.py` executes the following steps:
1. **Normalization:** The base64 header is stripped via regex, decoded, and converted to an RGB `PIL.Image` resized to a standard $112 \times 112$ resolution.
2. **Spatial Block Feature Grid:** The image is divided into a $4 \times 4$ grid of blocks, each sized $28 \times 28$ pixels.
3. **Feature Extraction:** Across each of the 16 blocks, 8 specific statistical and gradient features are extracted:
   - Grayscale block mean (`mean_val`)
   - Grayscale block standard deviation (`std_val`)
   - Horizontal edge gradient energy ($\frac{1}{N}\sum |\frac{\partial I}{\partial x}|$)
   - Vertical edge gradient energy ($\frac{1}{N}\sum |\frac{\partial I}{\partial y}|$)
   - Color channel means ($R_{mean}, G_{mean}, B_{mean}$)
   - Color dispersion (`color_var` across RGB)
4. **Vector Normalization:** $16 \text{ blocks} \times 8 \text{ features} = 128 \text{ dimensions}$. The resulting 128-d vector is $L_2$-normalized:
   $$\mathbf{v}_{norm} = \frac{\mathbf{v}}{\|\mathbf{v}\|_2}$$
5. **Cosine Similarity Evaluation:** For a gallery of enrolled student vectors, similarity is calculated as:
   $$\text{Similarity}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2}$$
   Matches meeting the threshold of $\ge 0.70$ are verified as authenticated biometric matches.

---

### Question 2: How does the Academic Risk Predictor work in `risk_service.py`?
**Answer:**
`AcademicRiskPredictor` implements an academic penalty scoring model:
$$\text{Total Penalty} = (\Delta_{att} \times 0.45) + (\Delta_{mid} \times 0.25) + (\Delta_{ass} \times 0.15) + \min(30.0, \text{backlogs} \times 15.0)$$
Where:
- $\Delta_{att} = \max(0.0, 100.0 - \text{attendance\_rate})$
- $\Delta_{mid} = \max(0.0, 100.0 - \text{midterm\_score})$
- $\Delta_{ass} = \max(0.0, 100.0 - \text{assignment\_score})$

**Risk Classification:**
- **High Risk:** $\text{Risk Score} \ge 0.65$, or attendance $< 75.0\%$, or backlogs $\ge 2$. Flags remedial mentoring and parent notifications.
- **Medium Risk:** $\text{Risk Score} \ge 0.35$, or attendance $< 80.0\%$, or backlogs $== 1$. Suggests advisor check-in.
- **Low Risk:** On track for academic honors.

---

### Question 3: Describe a tough edge-case bug you fixed in `smartcampus-ai`.
**Answer:**
**The Bug:** During Day 8 testing, when a student initially pre-marked as "absent" by faculty arrived late and scanned their face on the webcam, the `/api/v1/attendance/mark` endpoint returned an HTTP 400 with the message *"Attendance already marked for today"*.  
**Root Cause:** The database query filtered for any existing record on that calendar day and rejected new submissions regardless of status.  
**The Solution:** I modified the attendance endpoint logic to check the current status of the record. If the status is `'absent'`, the endpoint updates the existing row to `'present'`, updates the timestamp, logs the face confidence score, and returns an HTTP 200 with an `"attendance_updated"` event.

---

### Question 4: How does the CSV export endpoint stream data cleanly?
**Answer:**
The `/api/v1/attendance/export/csv` endpoint queries SQLite using SQLAlchemy sessions, streams rows using Python's `csv.writer` into an in-memory `io.StringIO` buffer, and returns a `StreamingResponse` (or `Response`) with media type `text/csv` and header:
`Content-Disposition: attachment; filename="attendance_report_<date>.csv"`
This prevents memory accumulation on large student datasets.
