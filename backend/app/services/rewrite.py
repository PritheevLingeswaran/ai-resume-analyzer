from __future__ import annotations

import re


def build_rewrite_suggestions(
    resume_text: str,
    job_description: str,
    role: str | None,
    missing_skills: list[str],
) -> dict[str, object]:
    role_name = role or "Target Role"
    headline_options = [
        f"{role_name} | Production ML Systems | ATS-Optimized Resume",
        f"{role_name} | Python | ML Systems | Deployment & Evaluation",
        f"{role_name} | Applied AI | Production Engineering | Data Pipelines",
    ]

    summary_rewrite = (
        f"{role_name} candidate with hands-on experience building production-grade machine learning systems, "
        "real-time pipelines, and measurable model evaluation workflows. Strongest visible strengths include "
        "Python, modern ML frameworks, system design thinking, and delivery backed by metrics."
    )
    if missing_skills:
        summary_rewrite += f" To improve ATS alignment further, make experience with {', '.join(missing_skills[:3])} more explicit where accurate."

    suggestions = [
        {
            "title": "Professional Summary Upgrade",
            "before": extract_summary(resume_text),
            "after": summary_rewrite,
            "rationale": "Moves the target role and strongest ATS signals into the first screen recruiters and parsers see.",
        },
        {
            "title": "Skills Section Upgrade",
            "before": "List core tools without explicit alignment to the job description.",
            "after": build_skill_line(job_description, missing_skills),
            "rationale": "Adds recruiter-friendly clustering and brings missing job keywords into a natural, honest structure.",
        },
        {
            "title": "Project Bullet Upgrade",
            "before": "Built ML systems with measurable improvements in latency and reliability.",
            "after": build_project_rewrite(role_name, missing_skills),
            "rationale": "Makes model deployment, evaluation, and business-facing engineering signals more obvious.",
        },
    ]

    return {
        "role": role,
        "summaryRewrite": summary_rewrite,
        "headlineOptions": headline_options,
        "suggestions": suggestions,
    }


def extract_summary(resume_text: str) -> str:
    match = re.search(r"summary\s+(.*?)\s+(technical skills|skills|projects)", resume_text, re.I | re.S)
    if match:
        return " ".join(match.group(1).split())[:320]
    return "Current summary could be stronger and more targeted to the role."


def build_skill_line(job_description: str, missing_skills: list[str]) -> str:
    base = "Core: Python, C++, PyTorch, TensorFlow, Scikit-learn, Pandas, Statistics, Git, REST APIs, CI/CD"
    if missing_skills:
        base += f" | Add explicitly where true: {', '.join(missing_skills[:3])}"
    if "graphql" in job_description.lower():
        base += " | APIs: REST, GraphQL"
    return base


def build_project_rewrite(role_name: str, missing_skills: list[str]) -> str:
    missing_note = ""
    if missing_skills:
        missing_note = f" The bullet should also explicitly mention {', '.join(missing_skills[:2])} if that work is genuinely represented."
    return (
        f"Designed and deployed production-ready ML services for {role_name} use cases, combining model evaluation, "
        "low-latency APIs, monitoring, and reliability-focused engineering backed by quantified outcomes."
        f"{missing_note}"
    )
