# Handled (MVP)

Life admin, executed — approval-first workflows for reimbursements, scheduling, government forms, and simple tax filing.

## Prereqs
- Node 18+
- Python 3.11+
- Postgres (recommended)

## Backend
```bash
cd backend
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In dev, magic links are printed to the backend console.

## Frontend
```bash
cd frontend
npm install
export NEXT_PUBLIC_API_BASE=http://localhost:8000
npm run dev
```

Open http://localhost:3000

## Next upgrades
- Replace tick button with background jobs
- Wire OCR + OpenAI extraction
- Add human review queue
- Add portal automation (Playwright)
