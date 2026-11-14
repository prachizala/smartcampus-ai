# SmartCampus AI: 3-Minute Video Demo Script

**Speaker**: Prachi Zala  
**Target Audience**: Interviewers, Faculty, Technical Evaluators  

### [00:00 - 00:30] Introduction & Problem
"Hello! I'm Prachi Zala, and today I'm presenting **SmartCampus AI**. In colleges, taking attendance manually wastes 15 minutes of every lecture, and paper sign-ins make proxy attendance trivial. Worse, professors only discover students failing or dropping out after semester exams when it's too late. SmartCampus AI solves both problems."

### [00:30 - 01:30] Biometric Face Attendance
"Here is our faculty command center. As students enter the lecture, our webcam scanner captures each face, extracts a 128-dimensional spatial feature vector, and compares it against enrolled student embeddings using cosine similarity. If similarity exceeds 70%, attendance is marked in under 50 milliseconds with duplicate suppression."

### [01:30 - 02:15] Early Risk Warning ML Engine
"Beside attendance, our scikit-learn style ML risk classifier continuously evaluates four student metrics: attendance percentage, midterm assessment scores, assignment completion, and active backlogs. Notice how Kabir Mehta is flagged as High Risk because his attendance dropped below 75% with two backlogs. The faculty can generate an academic mentoring slip with one click."

### [02:15 - 03:00] Architecture & Testing
"Under the hood, the backend is built with FastAPI, SQLAlchemy, and Pydantic, tested with pytest, and containerized via Docker. All code follows clean architecture and is ready for production PostgreSQL deployment. Thank you!"
