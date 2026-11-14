# Deployment Guide: SmartCampus AI

### Architecture
- Web Server: Uvicorn (ASGI)
- Container: Docker multi-stage build
- Port: 8000

### Production Checklist
1. Set `DEBUG=False` in `.env`.
2. Generate a secure random string for `SECRET_KEY`.
3. Set `DATABASE_URL` to a production PostgreSQL instance:
   `postgresql://user:password@host:5432/smartcampus`
4. Run database migrations and seed script.
5. Deploy using `docker-compose up -d`.
