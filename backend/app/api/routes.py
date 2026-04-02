from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR, get_settings
from app.db.database import get_db
from app.db.models import AnalysisResult, JobPosting, Resume
from app.schemas import (
    AnalyzeRequest,
    AnalysisBreakdown,
    AnalysisResponse,
    AuditSection,
    HealthResponse,
    ReportListItem,
    ReportMeta,
    RewriteResponse,
    ScoreExplanation,
    SectionInsight,
    SkillGroup,
    UploadResponse,
)
from app.services.analysis import analyze_resume, build_audit_sections, build_section_insights, compute_semantic_fit
from app.services.document_parser import DocumentParserError, extract_text
from app.services.llm import maybe_refine_with_llm
from app.services.rewrite import build_rewrite_suggestions


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
def analyze(payload: AnalyzeRequest, request: Request, db: Session = Depends(get_db)):
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

    return _serialize_result(result, request)


@router.get("/result/{result_id}", response_model=AnalysisResponse)
def get_result(result_id: int, request: Request, db: Session = Depends(get_db)):
    result = db.get(AnalysisResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis result not found.")
    return _serialize_result(result, request)


@router.get("/reports", response_model=list[ReportListItem])
def list_reports(request: Request, limit: int = 10, db: Session = Depends(get_db)):
    settings = get_settings()
    limit = max(1, min(50, limit))
    stmt = (
        select(AnalysisResult)
        .order_by(AnalysisResult.created_at.desc())
        .limit(limit)
    )
    results = db.scalars(stmt).all()
    items: list[ReportListItem] = []
    for result in results:
        audit_payload = build_audit_sections(
            role=result.job.role if result.job else None,
            ats_score=round(result.ats_score),
            matched=_deserialize_list(result.matched_skills),
            missing=_deserialize_list(result.missing_skills),
            strengths=_deserialize_list(result.strengths),
            risks=_deserialize_list(result.risks),
            breakdown={
                "keywordCoverage": round(result.keyword_coverage, 2),
                "sectionScore": round(result.section_score, 2),
                "impactScore": round(result.impact_score, 2),
                "formattingScore": round(result.formatting_score, 2),
                "semanticFit": compute_semantic_fit(
                    result.resume.extracted_text if result.resume else "",
                    result.job.description if result.job else "",
                ),
            },
            suggestions=result.suggestions,
        )
        items.append(
            ReportListItem(
                id=result.id,
                role=result.job.role if result.job else None,
                ats_score=round(result.ats_score),
                summaryHeadline=audit_payload["summaryHeadline"],
                createdAt=result.created_at,
                shareUrl=_share_url(settings, result.id, request),
            )
        )
    return items


@router.get("/result/{result_id}/rewrite", response_model=RewriteResponse)
def rewrite_report(result_id: int, db: Session = Depends(get_db)):
    result = db.get(AnalysisResult, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis result not found.")
    payload = build_rewrite_suggestions(
        resume_text=result.resume.extracted_text if result.resume else "",
        job_description=result.job.description if result.job else "",
        role=result.job.role if result.job else None,
        missing_skills=_deserialize_list(result.missing_skills),
    )
    return RewriteResponse(**payload)


def _deserialize_list(raw: str) -> list[str]:
    try:
        value = json.loads(raw or "[]")
        return value if isinstance(value, list) else []
    except json.JSONDecodeError:
        return []


def _serialize_result(result: AnalysisResult, request: Request) -> AnalysisResponse:
    settings = get_settings()
    matched = _deserialize_list(result.matched_skills)
    missing = _deserialize_list(result.missing_skills)
    semantic_fit = compute_semantic_fit(
        result.resume.extracted_text if result.resume else "",
        result.job.description if result.job else "",
    )
    breakdown = {
        "keywordCoverage": round(result.keyword_coverage, 2),
        "sectionScore": round(result.section_score, 2),
        "impactScore": round(result.impact_score, 2),
        "formattingScore": round(result.formatting_score, 2),
        "semanticFit": round(semantic_fit, 2),
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
    section_payload = build_section_insights(
        resume_text=result.resume.extracted_text if result.resume else "",
        job_description=result.job.description if result.job else "",
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
        sections=[SectionInsight(**entry) for entry in section_payload],
        meta=ReportMeta(
            shareUrl=_share_url(settings, result.id, request),
            generatedForRole=result.job.role if result.job else None,
            createdAt=result.created_at,
        ),
        timestamp=result.created_at,
    )


def _share_url(settings, result_id: int, request: Request) -> str:
    configured_base = settings.public_app_url.rstrip("/")
    if _is_public_base_url(configured_base):
        base_url = configured_base
    else:
        base_url = _request_origin(request)
    return f"{base_url}/results.html?id={result_id}"


def _is_public_base_url(value: str) -> bool:
    return bool(value) and "localhost" not in value and "127.0.0.1" not in value


def _request_origin(request: Request) -> str:
    forwarded_proto = request.headers.get("x-forwarded-proto")
    forwarded_host = request.headers.get("x-forwarded-host")
    host = forwarded_host or request.headers.get("host") or request.url.netloc
    scheme = forwarded_proto or request.url.scheme
    return f"{scheme}://{host}".rstrip("/")
