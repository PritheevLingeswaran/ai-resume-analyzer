from __future__ import annotations

from app.core.config import Settings
from app.services.analysis import AnalysisOutcome


def maybe_refine_with_llm(
    outcome: AnalysisOutcome,
    settings: Settings,
    resume_text: str,
    job_description: str,
    job_role: str | None,
) -> AnalysisOutcome:
    if not settings.enable_llm_recommendations or not settings.openai_api_key:
        return outcome

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout_seconds,
            max_retries=0,
        )
        prompt = (
            "You are helping improve a resume for ATS and recruiter review.\n"
            f"Target role: {job_role or 'Not specified'}\n\n"
            f"Resume:\n{resume_text[:6000]}\n\n"
            f"Job description:\n{job_description[:6000]}\n\n"
            f"Current analysis summary: {outcome.summary}\n"
            f"Matched skills: {', '.join(outcome.matched_skills)}\n"
            f"Missing skills: {', '.join(outcome.missing_skills)}\n\n"
            "Return plain text with exactly two paragraphs. "
            "Paragraph 1: concise recruiter-style summary. "
            "Paragraph 2: practical suggestions without inventing experience."
        )
        response = client.responses.create(
            model=settings.openai_model,
            input=prompt,
        )
        text = (response.output_text or "").strip()
        if not text:
            return outcome

        parts = [part.strip() for part in text.split("\n\n") if part.strip()]
        summary = parts[0] if parts else outcome.summary
        suggestions = parts[1] if len(parts) > 1 else outcome.suggestions
        outcome.summary = summary
        outcome.suggestions = suggestions
        return outcome
    except Exception:
        return outcome
