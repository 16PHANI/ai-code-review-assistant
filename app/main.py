from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json
from groq import Groq
from datetime import datetime
from app.database import save_review, get_reviews, get_review_by_id

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=GROQ_API_KEY)

app = FastAPI(title="AI Code Review Assistant", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class CodeSubmission(BaseModel):
    code: str
    language: str
    session_id: Optional[str] = "default"


class ReviewResponse(BaseModel):
    id: str
    language: str
    issues: list
    suggestions: list
    overall_quality: str
    summary: str
    submitted_at: str


def parse_groq_response(language: str, code: str) -> dict:
    prompt = f"""You are an expert {language} code reviewer.

Review the following code and respond ONLY in this exact JSON format with no extra text:
{{
  "overall_quality": "Good",
  "summary": "One sentence overall assessment.",
  "issues": [
    {{"category": "Bug", "line": "1", "description": "description of the issue"}}
  ],
  "suggestions": [
    {{"title": "short title", "description": "actionable fix suggestion", "example": "fixed code snippet"}}
  ]
}}

overall_quality must be one of: Good, Needs Improvement, Poor
category must be one of: Bug, Performance, Security, Style, Logic

Code:
{code}

Return ONLY valid JSON. No markdown. No explanation."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=2048,
    )

    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])
    return json.loads(text.strip())


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/review", response_model=ReviewResponse)
async def review_code(submission: CodeSubmission):
    if not submission.code or len(submission.code.strip()) < 10:
        raise HTTPException(status_code=400, detail="Code must be at least 10 characters.")
    if len(submission.code) > 10000:
        raise HTTPException(status_code=400, detail="Code must be under 10,000 characters.")
    try:
        parsed = parse_groq_response(submission.language, submission.code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI review failed: {str(e)}")

    doc = {
        "session_id": submission.session_id,
        "language": submission.language,
        "code": submission.code,
        "issues": parsed.get("issues", []),
        "suggestions": parsed.get("suggestions", []),
        "overall_quality": parsed.get("overall_quality", "N/A"),
        "summary": parsed.get("summary", ""),
        "submitted_at": datetime.utcnow().isoformat()
    }
    saved_id = save_review(doc)
    return ReviewResponse(
        id=saved_id, language=doc["language"], issues=doc["issues"],
        suggestions=doc["suggestions"], overall_quality=doc["overall_quality"],
        summary=doc["summary"], submitted_at=doc["submitted_at"]
    )


@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    reviews = get_reviews(session_id)
    return {"session_id": session_id, "count": len(reviews), "reviews": reviews}


@app.get("/api/review/{review_id}")
async def get_single_review(review_id: str):
    review = get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")
    return review


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
