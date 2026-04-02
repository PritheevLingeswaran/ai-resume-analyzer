# AI Resume Analyzer

AI Resume Analyzer is a full-stack resume scoring and ATS-style review platform built with a static frontend and a Python FastAPI backend.

## Features

- Upload PDF and DOCX resumes
- Extract resume text automatically
- Analyze resume-job fit with ATS-style scoring
- Show matched skills, missing skills, strengths, risks, and score breakdowns
- Generate advanced AI-oriented audit sections for role targeting
- Serve both frontend and backend from one FastAPI app
- Deploy with Render or Docker

## Project Structure

- `frontend/` - static HTML, CSS, and JavaScript UI
- `backend/` - FastAPI API, analysis engine, persistence, and document parsing

## Local Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Open:

- Frontend: `http://localhost:8080/index.html`
- Dashboard: `http://localhost:8080/dashboard.html`
- Results: `http://localhost:8080/results.html`
- API docs: `http://localhost:8080/docs`

## Environment Variables

Configured through `backend/.env`.

Common keys:

- `SRA_OPENAI_API_KEY`
- `SRA_OPENAI_MODEL`
- `SRA_ENABLE_LLM_RECOMMENDATIONS`
- `SRA_DATABASE_URL`
- `SRA_PUBLIC_APP_URL`

## Deployment

### Render

This repo includes `render.yaml` at the root. Connect the GitHub repo in Render and set the required environment variables in the Render dashboard.

Set `SRA_PUBLIC_APP_URL` to your deployed frontend URL so share links point to the public site.

### Docker

```bash
cd backend
docker build -t ai-resume-analyzer .
docker run -p 8080:8080 --env-file .env ai-resume-analyzer
```

### Firebase Hosting

This repo includes Firebase Hosting config for the static frontend in `frontend/`.

```bash
npx firebase-tools deploy --only hosting
```

The hosted frontend defaults to mock API responses through `frontend/js/deploy-config.js`. To connect it to a real backend later, set `BASE_URL` in that file to your deployed API origin and redeploy.
