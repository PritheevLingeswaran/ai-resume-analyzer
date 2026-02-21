# Smart Resume Analyzer — Full Stack (Frontend + Backend + Docker)

A complete, production‑ready project: **Bootstrap frontend**, **Java 17 + Spring Boot backend**, **SQLite** DB, **OpenNLP** + **OpenAI** integration, **Log4j2** logging, **JUnit 5** tests, and **Docker** containerization.

## Folder Structure
```
smart-resume-analyzer/
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── results.html
│   ├── about.html
│   ├── css/
│   ├── js/
│   └── mocks/
├── backend/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .env
│   ├── logs/
│   ├── data/
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/sra/backend/...
│       ├── main/resources/
│       └── test/java/com/sra/backend/...
└── README.md
```

---

## Backend (Java + Maven)

### Build & Test
```bash
cd backend
mvn clean test
mvn clean package
```
The JAR lands in `backend/target/`.

### Run locally
```bash
java -jar target/smart-resume-analyzer-backend-1.0.0.jar
```
Server at `http://localhost:8080`.

### Environment
- `SRA_DB_PATH` — SQLite path (default: `data/smart_resume_analyzer.db`)
- `OPENAI_API_KEY` — optional: enables real OpenAI suggestions (fallback otherwise)
- `spring.servlet.multipart.max-file-size` — file upload limit

### Logging
- **Console** and **file** logs (`backend/logs/app.log`, rotated) via Log4j2.

### API Endpoints
- `POST /api/upload` — multipart `file` (PDF/DOCX ≤ 5MB) → `{ fileName, extractedText, resumeId }`
- `POST /api/analyze` — JSON `{ resumeText, jobDescription, jobRole }` → `{ ats_score, matchedSkills, missingSkills, suggestions, summary, resultId }`
- `GET  /api/result/{id}` — retrieve stored result
- `GET  /api/jobs` — predefined roles

**Errors**: returns JSON `{ "error": "..." }` with appropriate HTTP code (400/500).

---

## Docker

### Compose (recommended)
```bash
cd backend
cp .env .env.local  # or edit .env directly
docker-compose up --build -d
```
- Backend: `http://localhost:8080`
- Data volume: `./data` ↔ `/app/data`
- Logs: `./logs` ↔ `/app/logs`

### Health Check
```bash
docker logs -f sra-backend
```

### Inspect DB
```bash
docker exec -it sra-sqlite-cli sqlite3 /data/smart_resume_analyzer.db ".tables"
```

### Stop
```bash
docker-compose down
```

---

## Frontend (HTML/CSS/JS + Bootstrap)

### Run locally (static server example)
Use any static server (VSCode Live Server, `python -m http.server`, etc.). Example:
```bash
cd frontend
python -m http.server 5500
```
Open `http://localhost:5500/index.html`.

**Point the frontend to Docker backend**:
- Default base URL is `http://localhost:8080` if served from `localhost`.
- Override: `?api=http://localhost:8080` or `localStorage.setItem('SRA_BASE_URL','http://localhost:8080')`
- Offline mocks: `?mocks=1` or `localStorage.setItem('SRA_USE_MOCKS','true')`

### UX Flow
1) Upload resume (PDF/DOCX) → extracted text appears.  
2) Paste JD + choose role (or “Other”).  
3) Click **Analyze** → loading overlay → results page updates with ATS, matched/missing, suggestions, summary.  
4) Download JSON / PDF print.

---

## Testing

### Unit tests (JUnit 5 + Mockito)
- ResumeService: Tika extraction from in‑memory DOCX.
- NLPService: tokenization + keyword extraction.
- AIService: adapter & fallback paths (no real network).
- AnalysisService: ATS score + matched/missing + validation.
- DAO: SQLite CRUD (file DB under `target/test-db/`).

Run:
```bash
cd backend
mvn clean test
```

---

## Notes
- To enable POS tagging, place `en-pos-maxent.bin` under `backend/src/main/resources/models/`.
- CORS is allowed for all origins (`@CrossOrigin("*")`) to simplify local dev. Tighten in production.
- For production hosting, consider Nginx as a reverse proxy (serve frontend + proxy `/api/*` to backend).

Enjoy building 🚀
