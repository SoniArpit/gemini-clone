# GemChatRoom

A Gemini-powered chatroom backend with user authentication, chat management, AI integration, and subscription support.

---

## Table of Contents

- [Directory Structure](#directory-structure)
- [Setup & Run](#setup--run)
- [Architecture Overview](#architecture-overview)
- [Queue System (Celery)](#queue-system-celery)
- [Gemini API Integration](#gemini-api-integration)
- [Assumptions & Design Decisions](#assumptions--design-decisions)
- [API Usage & Postman Testing](#api-usage--postman-testing)
- [Access & Deployment](#access--deployment)

---

## Directory Structure

```
GemChatRoom/
├── alembic/                # Database migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── fb3d0fc6ae00_init_schema.py
├── alembic.ini             # Alembic config
├── app/                    # Main application code
│   ├── api/                # API routers
│   │   ├── api.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── chatroom.py
│   │       ├── health.py
│   │       ├── message.py
│   │       ├── subscription.py
│   │       ├── test.py
│   │       └── user.py
│   ├── core/               # Config, DB, Celery
│   │   ├── celery_app.py
│   │   ├── config.py
│   │   └── db.py
│   ├── models/             # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── chatroom.py
│   │   ├── message.py
│   │   └── user.py
│   ├── schemas/            # Pydantic schemas
│   │   ├── auth.py
│   │   ├── chatroom.py
│   │   ├── common.py
│   │   ├── message.py
│   │   ├── subscription.py
│   │   └── user.py
│   ├── services/           # Business logic
│   │   ├── auth.py
│   │   ├── chatroom.py
│   │   ├── gemini.py
│   │   ├── hash.py
│   │   ├── jwt.py
│   │   ├── message.py
│   │   ├── otp.py
│   │   └── subscription.py
│   ├── tasks/              # Celery tasks
│   │   ├── __init__.py
│   │   └── gemini_tasks.py
│   ├── utils/              # Utility functions
│   │   └── dependencies.py
│   └── main.py             # FastAPI entrypoint
├── Procfile                # For deployment (e.g., Heroku)
├── README.md
├── requirements.txt
├── script.sh
└── venv/                   # Python virtual environment
```

---

## Setup & Run

> **Alembic/env.py Customization:**
>
> - Ensure your `alembic/env.py` includes the following lines to load the database URL and models from your FastAPI app:
>   ```python
>   from app.core.config import settings
>   from app.core.db import Base
>   from app.models import *
>   config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
>   target_metadata = Base.metadata
>   ```
> - This ensures Alembic uses the correct database and models for migrations.

> **Alembic Configuration Note:**
>
> - Only `alembic/env.py` was changed to load the database URL from your `.env` (via `app/core/config.py`).
> - You do **not** need to manually edit `alembic.ini` for the database URL; it is ignored in favor of the dynamic value.
> - Ensure your `.env` is correctly configured before running migrations.

### 1. Clone & Install

```bash
git clone git@github.com:SoniArpit/gemini-clone.git
cd GemChatRoom
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root with the following (see `app/core/config.py`):

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300
OTP_EXPIRATION_MINUTES=5
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
GOOGLE_API_KEY=your_google_api_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PRO_PRICE_ID=your_stripe_price_id
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
STRIPE_SUCCESS_URL=http://localhost:8000/success
STRIPE_CANCEL_URL=http://localhost:8000/cancel
```

### 3. Database Migration

```bash
alembic revision --autogenerate -m "init schema"
```

```bash
alembic upgrade head
```

### 4. Start Services

- **API Server:**
  ```bash
  uvicorn app.main:app --reload
  ```
- **Celery Worker:**
  ```bash
  celery -A app.core.celery_app.celery_app worker --loglevel=info -Q gemini
  ```
- **Redis Server:**
  ```bash
  redis-server
  ```

---

## Architecture Overview

- **FastAPI**: Main web framework for API endpoints.
- **PostgreSQL**: Stores users, chatrooms, messages, subscriptions.
- **Redis**: Used for OTP, caching, and as Celery broker/result backend.
- **Celery**: Handles background tasks (e.g., AI message generation).
- **Stripe**: Manages Pro subscriptions and webhooks.
- **Google Gemini API**: Generates AI chat responses.

### Main Components

- `app/api/v1/`: API endpoints (auth, chatroom, message, subscription, user)
- `app/models/`: SQLAlchemy models
- `app/services/`: Business logic (auth, chat, gemini, etc.)
- `app/tasks/`: Celery tasks
- `app/core/`: Config, DB, Celery setup

---

## Queue System (Celery)

- **Setup:** See `app/core/celery_app.py`.
- **Broker/Backend:** Redis (configurable via env vars).
- **Task Routing:** All Gemini-related tasks routed to the `gemini` queue.
- **Example Task:**
  - `generate_reply_task` in `app/tasks/gemini_tasks.py` calls Gemini API and saves the response.
- **Usage:**
  - When a user sends a message, a Celery task is triggered to generate the AI reply asynchronously.

---

## Gemini API Integration

- **Library:** Uses `google-generativeai` Python SDK.
- **API Key:** Set via `GOOGLE_API_KEY` env variable.
- **Model:** `gemini-1.5-flash` (see `app/services/gemini.py`).
- **Error Handling:** Handles API errors, rate limits, safety blocks, and connection issues gracefully.
- **Flow:**
  1. User sends a message (API endpoint).
  2. Celery task (`generate_reply_task`) calls `call_gemini_api`.
  3. Gemini response is saved and returned to the user.

---

## Assumptions & Design Decisions

- **Authentication:** OTP-based signup via mobile number. JWT for session management.
- **User Tiers:** `basic` and `pro` (Pro via Stripe subscription).
- **AI Safety:** Handles Gemini safety blocks and errors.
- **Async Processing:** All AI responses are generated asynchronously via Celery.
- **Payments:** Stripe Checkout for Pro subscriptions; webhooks for event handling.
- **Extensibility:** Modular service and API structure for easy feature addition.

---

## API Usage & Postman Testing

**Postman Collection:**

- You can find a ready-to-use public Postman collection for this API here: [Gemini Clone API Postman Collection](https://www.postman.com/sudoarpit/public-workspace/collection/mki88zg/gemini-clone-api?action=share&creator=6225275)

**Swagger/OpenAPI Documentation:**

- View the live API docs here: [https://gemini-clone-yiem.onrender.com/docs](https://gemini-clone-yiem.onrender.com/docs)

### 1. Auth Flow

- `POST /api/v1/auth/signup` — Register with mobile
- `POST /api/v1/auth/send-otp` — Request OTP
- `POST /api/v1/auth/verify-otp` — Verify OTP, receive JWT
- `POST /api/v1/auth/forgot-password` — Request OTP for password reset
- `POST /api/v1/auth/change-password` — Change password (JWT required)

### 2. Chatroom

- `POST /api/v1/chatroom/` — Create chatroom (JWT required)
- `GET /api/v1/chatroom/` — List user chatrooms (JWT required)
- `GET /api/v1/chatroom/{chatroom_id}` — Get chatroom details (JWT required)

### 3. Messaging

- `POST /api/v1/message/chatroom/{chatroom_id}/message` — Send message to chatroom (JWT required)
  - Triggers Gemini AI reply via Celery

### 4. Subscription

- `POST /api/v1/subscription/subscribe/pro` — Start Pro subscription (Stripe Checkout, JWT required)
- `POST /api/v1/subscription/webhook/stripe` — Stripe webhook endpoint (no auth)
- `GET /api/v1/subscription/status` — Get current subscription status (JWT required)

### 5. User

- `GET /api/v1/user/me` — Get current user info (JWT required)

### 6. Health

- `GET /api/v1/health` — Health check

#### **Authentication in Postman**

- Obtain JWT via `/auth/verify-otp`.
- Set `Authorization: Bearer <token>` header for protected endpoints.

#### **Example Signup & Chat Flow**

1. `POST /api/v1/auth/signup` with `{ "mobile": "1234567890" }`
2. `POST /api/v1/auth/send-otp` with `{ "mobile": "1234567890" }`
3. `POST /api/v1/auth/verify-otp` with `{ "mobile": "1234567890", "otp": "<received_otp>" }` → Get `access_token`
4. Use `access_token` as Bearer token for chatroom/message endpoints

---
