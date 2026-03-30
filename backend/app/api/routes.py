from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR, get_settings
from app.db.database import get_db
from app.db.models import AnalysisResult, JobPosting, Resume
from app.schemas import AnalyzeRequest, AnalysisBreakdown, AnalysisResponse, AuditSection, HealthResponse, ScoreExplanation, SkillGroup, UploadResponse
from app.services.analysis import analyze_resume, build_audit_sections
from app.services.document_parser import DocumentParserError, extract_text
from app.services.llm import maybe_refine_with_llm


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def healthcheck():
    settings = get_settings()
    return HealthResponse(status="ok", app=settings.app_name, environment=settings.app_env)


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    settings = get_settings()

    if not file.filename:
        raise HTTPException(status_code=400, detail="A file is required.")

    extension = Path(file.filename).suffix.lower().lstrip(".")
    if extension not in settings.allowed_extensions:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    content = await file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail=f"File exceeds {settings.max_upload_size_mb}MB limit.")

    safe_name = f"{uuid4().hex}.{extension}"
    destination = UPLOAD_DIR / safe_name
    destination.write_bytes(content)

    try:
        extracted_text = extract_text(destination)
    except DocumentParserError as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    resume = Resume(
        file_name=file.filename,
        file_path=str(destination),
        mime_type=file.content_type,
        extracted_text=extracted_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return UploadResponse(
        resumeId=resume.id,
        fileName=resume.file_name or file.filename,
        extractedText=resume.extracted_text,
        createdAt=resume.created_at,
    )


@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def analyze(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    settings = get_settings()

    resume = Resume(
        file_name=None,
        file_path=None,
        mime_type="text/plain",
        extracted_text=payload.resumeText.strip(),
    )
    job = JobPosting(
        role=(payload.jobRole or "").strip() or None,
        description=payload.jobDescription.strip(),
    )
    db.add_all([resume, job])
    db.flush()

    outcome = analyze_resume(payload.resumeText, payload.jobDescription, payload.jobRole)
    outcome = maybe_refine_with_llm(outcome, settings, payload.resumeText, payload.jobDescription, payload.jobRole)

    result = AnalysisResult(
        resume_id=resume.id,
        job_id=job.id,
        **outcome.as_db_payload(),
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return _serialize_result(result)


@router.get("/result/{result_id}", response_model=AnalysisResponse)
def get_result(result_id: int, db: Session = Depends(get_db)):
    result = db.get(AnalysisResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis result not found.")
    return _serialize_result(result)


def _deserialize_list(raw: str) -> list[str]:
    try:
        value = json.loads(raw or "[]")
        return value if isinstance(value, list) else []
    except json.JSONDecodeError:
        return []


def _serialize_result(result: AnalysisResult) -> AnalysisResponse:
    matched = _deserialize_list(result.matched_skills)
    missing = _deserialize_list(result.missing_skills)
    breakdown = {
        "keywordCoverage": round(result.keyword_coverage, 2),
        "sectionScore": round(result.section_score, 2),
        "impactScore": round(result.impact_score, 2),
        "formattingScore": round(result.formatting_score, 2),
    }
    audit_payload = build_audit_sections(
        role=result.job.role if result.job else None,
        ats_score=round(result.ats_score),
        matched=matched,
        missing=missing,
        strengths=_deserialize_list(result.strengths),
        risks=_deserialize_list(result.risks),
        breakdown=breakdown,
        suggestions=result.suggestions,
    )
    return AnalysisResponse(
        id=result.id,
        resumeId=result.resume_id,
        jobId=result.job_id,
        ats_score=round(result.ats_score),
        matchedSkills=matched,
        missingSkills=missing,
        suggestions=result.suggestions,
        summary=result.summary,
        strengths=_deserialize_list(result.strengths),
        risks=_deserialize_list(result.risks),
        breakdown=AnalysisBreakdown(
            **breakdown,
        ),
        audit=AuditSection(
            matchedGroups=[SkillGroup(**group) for group in audit_payload["matchedGroups"]],
            missingGroups=[SkillGroup(**group) for group in audit_payload["missingGroups"]],
            quickWins=audit_payload["quickWins"],
            finalVerdict=audit_payload["finalVerdict"],
            scoreExplanations=[ScoreExplanation(**entry) for entry in audit_payload["scoreExplanations"]],
            atsRiskLevel=audit_payload["atsRiskLevel"],
            summaryHeadline=audit_payload["summaryHeadline"],
            priorityGapHeadline=audit_payload["priorityGapHeadline"],
            strengthHighlights=audit_payload["strengthHighlights"],
            riskHighlights=audit_payload["riskHighlights"],
            suggestionBullets=audit_payload["suggestionBullets"],
        ),
        timestamp=result.created_at,
    )
