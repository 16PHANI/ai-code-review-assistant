# AI Code Review Assistant

> Instant AI-powered code review in your browser. Paste code, get structured feedback — issues categorised by type, actionable suggestions with fix examples, powered by LLaMA3-70B via Groq.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-darkgreen?style=flat-square&logo=mongodb)
![Docker](https://img.shields.io/badge/Docker-ready-blue?style=flat-square&logo=docker)
![Groq](https://img.shields.io/badge/Groq-LLaMA3--70B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## What it does

Submit code in any of 9 languages and receive a structured AI review in under 3 seconds:

- **Issue detection** — categorised as Bug, Performance, Security, Style, or Logic
- **Fix suggestions** — with concrete code examples, not vague advice
- **Quality rating** — Good / Needs Improvement / Poor with a one-line summary
- **Session history** — reviews stored per session in MongoDB
- **REST API** — full OpenAPI/Swagger documentation at `/docs`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| AI Model | LLaMA3-70B via Groq API |
| Database | MongoDB 7.0 |
| Frontend | HTML5, CSS3, JavaScript (vanilla) |
| Container | Docker, Docker Compose |
| Deployment | GCP Cloud Run |

---

## Architecture

```
+------------------------------------------+
|              Browser (Client)            |
|  HTML + CSS + Vanilla JS                 |
|  - Code editor with line numbers         |
|  - REST calls via Fetch API              |
+--------------------+---------------------+
                     | HTTP POST /api/review
+--------------------v---------------------+
|           FastAPI Backend                |
|  - Input validation (length, type)       |
|  - Prompt engineering for LLaMA3        |
|  - JSON schema enforcement               |
|  - CORS middleware                       |
|  - Static file serving (Jinja2)          |
+-------+-----------------------+----------+
        |                       |
+-------v-------+   +-----------v---------+
|   Groq API    |   |      MongoDB        |
|  LLaMA3-70B   |   |  - Review storage   |
|  <3s avg      |   |  - Session history  |
+---------------+   +---------------------+
```

---

## API Reference

### POST `/api/review`
Submit code for review.

**Request:**
```json
{
  "code": "def add(a, b):\n    return a+b",
  "language": "Python",
  "session_id": "session_abc123"
}
```

**Response:**
```json
{
  "id": "664abc123def456",
  "language": "Python",
  "overall_quality": "Good",
  "summary": "Clean, minimal function with no issues.",
  "issues": [],
  "suggestions": [
    {
      "title": "Add type hints",
      "description": "Add type annotations for better readability.",
      "example": "def add(a: int, b: int) -> int:"
    }
  ],
  "submitted_at": "2026-05-04T20:47:34.086Z"
}
```

**Issue categories:** `Bug` `Performance` `Security` `Style` `Logic`

**Quality values:** `Good` `Needs Improvement` `Poor`

---

### GET `/api/history/{session_id}`
All reviews for a session (code excluded for privacy).

### GET `/api/review/{review_id}`
Specific review by MongoDB ObjectId.

### GET `/health`
Returns `{"status": "ok", "version": "1.0.0"}`

### GET `/docs`
Interactive Swagger UI.

---

## Local Setup

### Prerequisites
- Docker Desktop
- Groq API key — free at https://console.groq.com

### Run

```bash
git clone https://github.com/16PHANI/ai-code-review-assistant.git
cd ai-code-review-assistant
echo GROQ_API_KEY=your_key_here> groq.env
docker-compose up --build
```

Open http://localhost:8080

### Without Docker

```bash
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here
export MONGO_URI=mongodb://localhost:27017
uvicorn app.main:app --reload --port 8080
```

---

## Project Structure

```
ai-code-review-assistant/
├── app/
│   ├── main.py        # FastAPI app, routes, Groq integration
│   ├── database.py    # MongoDB CRUD
│   └── __init__.py
├── templates/
│   └── index.html     # Frontend
├── static/
│   ├── css/style.css  # Dark terminal UI
│   └── js/app.js      # Frontend logic
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Deploy to GCP Cloud Run

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-code-review-assistant
gcloud run deploy ai-code-review-assistant \
  --image gcr.io/YOUR_PROJECT_ID/ai-code-review-assistant \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=your_key,MONGO_URI=your_atlas_uri
```

For production MongoDB use MongoDB Atlas free tier: https://www.mongodb.com/cloud/atlas

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key | Yes |
| `MONGO_URI` | MongoDB URI | Yes (default: localhost) |

---

## Supported Languages

Python · JavaScript · TypeScript · Java · C++ · Go · Rust · SQL · Other

---

## License

MIT

---

## Author

**Boyinapalli Phani Shankar**
GitHub: https://github.com/16PHANI
LinkedIn: https://linkedin.com/in/phanishankar16
Google Cloud Skills Boost: Gold League · 88,980 pts
