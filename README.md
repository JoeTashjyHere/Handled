# Handled

Handled is an AI-powered life admin execution platform. This monorepo includes a Next.js
frontend, a FastAPI backend, background workflows, and the infrastructure hooks needed for
magic-link auth, AI summarization, and S3-compatible storage.

## Repo structure

```
/
  frontend/
    app/
    components/
    lib/
  backend/
    main.py
    agents/
    workflows/
    models/
    services/
    db/
  README.md
```

## Environment variables

Copy `.env.example` to `.env` and fill in values as needed.

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o/5 models. |
| `OPENAI_MODEL` | Model name (ex: `gpt-4o`). |
| `DATABASE_URL` | PostgreSQL connection string. |
| `CELERY_BROKER_URL` | Redis broker for Celery. |
| `CELERY_BACKEND_URL` | Redis backend for Celery. |
| `SENDGRID_API_KEY` | SendGrid key for magic-link email delivery. |
| `FROM_EMAIL` | Sender address for magic-link emails. |
| `S3_ENDPOINT` | S3-compatible endpoint. |
| `S3_ACCESS_KEY` | Access key for object storage. |
| `S3_SECRET_KEY` | Secret key for object storage. |
| `S3_BUCKET` | Bucket name. |
| `NEXT_PUBLIC_API_BASE_URL` | Base URL for the backend API. |

## Local development

### Backend (FastAPI + Celery)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run the API
uvicorn main:app --reload --port 8000
```

In another terminal, run the Celery worker:

```bash
cd backend
source .venv/bin/activate
celery -A workflows.celery_app.celery_app worker --loglevel=info
```

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`, and it expects the backend
running at `http://localhost:8000`.

## Notes

- Magic-link auth is implemented via SendGrid in `backend/services/email.py`.
- AI summarization uses the OpenAI SDK in `backend/services/openai_client.py`.
- S3-compatible uploads are available in `backend/services/storage.py`.
