# NovaTrack API

Enterprise-grade work management and task tracking platform.

## Architecture & Tech Stack
- FastAPI
- PostgreSQL
- Redis
- Celery
- Docker

## Technical Specification for Website Launch
- RESTful API design with JWT-based RBAC
- Strict status transition engine for task lifecycle
- Activity audit logging
- Automatic daily cron job for the script (via Celery Beat) to process background analytics and status updates
- Containerized deployment pipeline