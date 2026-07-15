# NovaTrack API 🚀

Enterprise-grade REST API for project and task management. Built with a focus on high performance, scalability, and strict production-ready standards.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg)
![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)
![Celery](https://img.shields.io/badge/Celery-5.4.0-37814A.svg)

## ✨ Features

* **Authentication & Authorization:** Secure JWT-based auth, password recovery flow, and role-based access control (Admin/Member).
* **High Performance:** Asynchronous endpoints, database connection pooling, and Redis caching.
* **Background Processing:** Heavy tasks (PDF generation, Email sending) are offloaded to Celery workers via Redis message broker.
* **SaaS Ready:** Integrated Stripe Checkout and Webhooks for PRO subscriptions.
* **Full-Text Search:** Optimized SQL queries with `ILIKE` for rapid task searching.
* **Production Security:** API Rate Limiting (SlowAPI), CORS management, and Nginx reverse proxy configurations.
* **Observability:** Centralized logging with Loguru, intelligent healthchecks, and Sentry integration for real-time error tracking.

## 🏗️ Architecture & Tech Stack

* **Framework:** FastAPI
* **Database & ORM:** PostgreSQL, SQLAlchemy 2.0, Alembic (Migrations)
* **Caching & Broker:** Redis
* **Task Queue:** Celery
* **Containerization:** Docker, Docker Compose
* **Payment Gateway:** Stripe API
* **Error Tracking:** Sentry

## 🛠️ Local Development

### Prerequisites
* Docker and Docker Compose
* Python 3.12+ (for running outside of containers)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Miki-Zn/novatrack-api.git](https://github.com/your-username/novatrack-api.git)
   cd novatrack-api