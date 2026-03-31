from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SkillDefinition:
    key: str
    label: str
    aliases: tuple[str, ...]
    category: str


SKILL_CATALOG: tuple[SkillDefinition, ...] = (
    SkillDefinition("python", "Python", ("python",), "Programming"),
    SkillDefinition("cpp", "C++", ("c++", "cpp"), "Programming"),
    SkillDefinition("java", "Java", ("java",), "Programming"),
    SkillDefinition("javascript", "JavaScript", ("javascript", "js"), "Programming"),
    SkillDefinition("typescript", "TypeScript", ("typescript", "ts"), "Programming"),
    SkillDefinition("sql", "SQL", ("sql",), "Data"),
    SkillDefinition("postgresql", "PostgreSQL", ("postgresql", "postgres"), "Data"),
    SkillDefinition("mysql", "MySQL", ("mysql",), "Data"),
    SkillDefinition("mongodb", "MongoDB", ("mongodb", "mongo db", "mongo"), "Data"),
    SkillDefinition("redis", "Redis", ("redis",), "Data"),
    SkillDefinition("docker", "Docker", ("docker", "containerization", "containerized", "containerized services"), "Cloud"),
    SkillDefinition("kubernetes", "Kubernetes", ("kubernetes", "k8s"), "Cloud"),
    SkillDefinition("aws", "AWS", ("aws", "amazon web services"), "Cloud"),
    SkillDefinition("azure", "Azure", ("azure",), "Cloud"),
    SkillDefinition("gcp", "GCP", ("gcp", "google cloud", "google cloud platform"), "Cloud"),
    SkillDefinition("terraform", "Terraform", ("terraform",), "Cloud"),
    SkillDefinition("model_deployment", "Model Deployment", ("model deployment", "production deployment", "deploy ml models", "model serving", "production environments"), "Cloud"),
    SkillDefinition("airflow", "Airflow", ("airflow", "apache airflow"), "Data Engineering"),
    SkillDefinition("spark", "Spark", ("spark", "apache spark", "pyspark"), "Data Engineering"),
    SkillDefinition("hadoop", "Hadoop", ("hadoop",), "Data Engineering"),
    SkillDefinition("kafka", "Kafka", ("kafka", "apache kafka"), "Data Engineering"),
    SkillDefinition("data_pipelines", "Data Pipelines", ("data pipeline", "data pipelines", "data ingestion", "preprocessing", "data cleaning"), "Data Engineering"),
    SkillDefinition("react", "React", ("react", "react.js"), "Frontend"),
    SkillDefinition("nextjs", "Next.js", ("next.js", "nextjs"), "Frontend"),
    SkillDefinition("nodejs", "Node.js", ("node.js", "nodejs"), "Backend"),
    SkillDefinition("express", "Express", ("express", "express.js"), "Backend"),
    SkillDefinition("fastapi", "FastAPI", ("fastapi",), "Backend"),
    SkillDefinition("django", "Django", ("django",), "Backend"),
    SkillDefinition("flask", "Flask", ("flask",), "Backend"),
    SkillDefinition("spring_boot", "Spring Boot", ("spring boot",), "Backend"),
    SkillDefinition("rest_api", "REST APIs", ("rest api", "rest apis", "restful api", "api development"), "Backend"),
    SkillDefinition("graphql", "GraphQL", ("graphql",), "Backend"),
    SkillDefinition("microservices", "Microservices", ("microservices", "micro services"), "Architecture"),
    SkillDefinition("system_design", "System Design", ("system design",), "Architecture"),
    SkillDefinition("api_design", "API Design", ("api design",), "Architecture"),
    SkillDefinition("algorithms", "Algorithms", ("algorithms", "algorithmic logic", "computational problems"), "Architecture"),
    SkillDefinition("data_structures", "Data Structures", ("data structures", "trees", "graphs"), "Architecture"),
    SkillDefinition("git", "Git", ("git", "version control"), "Tooling"),
    SkillDefinition("github", "GitHub", ("github",), "Tooling"),
    SkillDefinition("gitlab", "GitLab", ("gitlab",), "Tooling"),
    SkillDefinition("cicd", "CI/CD", ("ci/cd", "cicd", "continuous integration", "continuous delivery", "github actions", "deployment pipeline"), "Tooling"),
    SkillDefinition("jenkins", "Jenkins", ("jenkins",), "Tooling"),
    SkillDefinition("testing", "Testing", ("testing", "test automation"), "Quality"),
    SkillDefinition("pytest", "Pytest", ("pytest",), "Quality"),
    SkillDefinition("unit_testing", "Unit Testing", ("unit testing", "unit tests"), "Quality"),
    SkillDefinition("machine_learning", "Machine Learning", ("machine learning", "ml"), "AI/ML"),
    SkillDefinition("deep_learning", "Deep Learning", ("deep learning", "deep learning networks", "neural network", "neural networks"), "AI/ML"),
    SkillDefinition("nlp", "NLP", ("nlp", "natural language processing"), "AI/ML"),
    SkillDefinition("tensorflow", "TensorFlow", ("tensorflow",), "AI/ML"),
    SkillDefinition("pytorch", "PyTorch", ("pytorch",), "AI/ML"),
    SkillDefinition("scikit_learn", "Scikit-learn", ("scikit-learn", "sklearn"), "AI/ML"),
    SkillDefinition("model_evaluation", "Model Evaluation", ("model evaluation", "evaluation systems", "llm evaluation"), "AI/ML"),
    SkillDefinition("monitoring", "Monitoring", ("monitoring", "prometheus", "metrics tracking", "model performance"), "AI/ML"),
    SkillDefinition("drift_detection", "Drift Detection", ("data drifts", "drift detection", "concept drift"), "AI/ML"),
    SkillDefinition("rag", "RAG", ("rag", "retrieval augmented generation"), "AI/ML"),
    SkillDefinition("pandas", "Pandas", ("pandas",), "Data"),
    SkillDefinition("numpy", "NumPy", ("numpy",), "Data"),
    SkillDefinition("linear_algebra", "Linear Algebra", ("linear algebra",), "Data"),
    SkillDefinition("calculus", "Calculus", ("calculus",), "Data"),
    SkillDefinition("probability", "Probability", ("probability",), "Data"),
    SkillDefinition("statistics", "Statistics", ("statistics", "statistical analysis"), "Data"),
    SkillDefinition("data_analysis", "Data Analysis", ("data analysis",), "Data"),
    SkillDefinition("data_visualization", "Data Visualization", ("data visualization", "visualization"), "Data"),
    SkillDefinition("power_bi", "Power BI", ("power bi",), "Analytics"),
    SkillDefinition("tableau", "Tableau", ("tableau",), "Analytics"),
    SkillDefinition("excel", "Excel", ("excel",), "Analytics"),
    SkillDefinition("linux", "Linux", ("linux",), "Tooling"),
    SkillDefinition("html", "HTML", ("html",), "Frontend"),
    SkillDefinition("css", "CSS", ("css",), "Frontend"),
    SkillDefinition("bootstrap", "Bootstrap", ("bootstrap",), "Frontend"),
)

SKILL_LOOKUP = {skill.key: skill for skill in SKILL_CATALOG}

ROLE_PROFILES: dict[str, dict[str, int]] = {
    "software engineer": {
        "python": 3,
        "cpp": 3,
        "java": 3,
        "sql": 3,
        "system_design": 3,
        "algorithms": 3,
        "data_structures": 3,
        "git": 2,
        "testing": 2,
        "rest_api": 2,
    },
    "backend developer": {
        "python": 4,
        "fastapi": 4,
        "django": 3,
        "flask": 3,
        "sql": 4,
        "postgresql": 4,
        "docker": 4,
        "aws": 3,
        "microservices": 3,
        "rest_api": 4,
        "api_design": 3,
        "testing": 2,
        "cicd": 2,
    },
    "frontend developer": {
        "javascript": 4,
        "typescript": 4,
        "react": 4,
        "nextjs": 3,
        "html": 4,
        "css": 4,
        "bootstrap": 2,
        "git": 2,
    },
    "full stack developer": {
        "javascript": 4,
        "typescript": 4,
        "react": 4,
        "nodejs": 3,
        "python": 3,
        "sql": 4,
        "rest_api": 3,
        "docker": 2,
    },
    "data analyst": {
        "sql": 4,
        "excel": 4,
        "power_bi": 4,
        "tableau": 4,
        "statistics": 3,
        "data_analysis": 4,
        "data_visualization": 3,
        "python": 2,
    },
    "ai/ml engineer": {
        "python": 5,
        "cpp": 3,
        "machine_learning": 5,
        "deep_learning": 4,
        "nlp": 3,
        "tensorflow": 4,
        "pytorch": 4,
        "scikit_learn": 4,
        "pandas": 4,
        "numpy": 3,
        "statistics": 4,
        "probability": 3,
        "linear_algebra": 3,
        "calculus": 3,
        "algorithms": 3,
        "data_structures": 3,
        "data_pipelines": 3,
        "model_deployment": 3,
        "monitoring": 3,
        "drift_detection": 3,
        "model_evaluation": 3,
        "docker": 3,
        "aws": 3,
        "azure": 2,
        "gcp": 2,
        "git": 2,
        "cicd": 3,
        "rest_api": 2,
        "graphql": 1,
    },
    "devops engineer": {
        "docker": 5,
        "kubernetes": 5,
        "aws": 4,
        "azure": 3,
        "gcp": 3,
        "terraform": 4,
        "cicd": 4,
        "jenkins": 3,
        "linux": 3,
        "git": 2,
    },
}

ROLE_ALIASES: dict[str, tuple[str, ...]] = {
    "software engineer": ("software engineer", "software developer", "sde"),
    "backend developer": ("backend developer", "backend engineer", "python backend developer"),
    "frontend developer": ("frontend developer", "front end developer", "frontend engineer", "front end engineer"),
    "full stack developer": ("full stack developer", "full stack engineer", "fullstack developer", "fullstack engineer"),
    "data analyst": ("data analyst", "business analyst", "analytics analyst"),
    "ai/ml engineer": (
        "ai/ml engineer",
        "ai engineer",
        "ml engineer",
        "machine learning engineer",
        "artificial intelligence engineer",
        "machine learning developer",
    ),
    "devops engineer": ("devops engineer", "devops", "site reliability engineer", "sre"),
}

SECTION_PATTERNS = {
    "summary": re.compile(r"\b(summary|profile|objective)\b", re.I),
    "experience": re.compile(r"\b(experience|employment|work history)\b", re.I),
    "skills": re.compile(r"\b(skills|technical skills|core competencies)\b", re.I),
    "projects": re.compile(r"\b(projects|personal projects)\b", re.I),
    "education": re.compile(r"\b(education|academic)\b", re.I),
    "certifications": re.compile(r"\b(certifications|licenses|certificates)\b", re.I),
}

ACTION_VERBS = {
    "built",
    "developed",
    "implemented",
    "led",
    "improved",
    "designed",
    "optimized",
    "deployed",
    "created",
    "launched",
    "delivered",
    "managed",
    "automated",
    "reduced",
    "increased",
}

WEAK_PATTERNS = (
    re.compile(r"\bresponsible for\b", re.I),
    re.compile(r"\bworked on\b", re.I),
    re.compile(r"\bhelped with\b", re.I),
)

SEMANTIC_SIGNAL_MAP: dict[str, tuple[str, ...]] = {
    "docker": ("containerization", "containerized", "dockerized"),
    "cicd": ("github actions", "deployment pipeline", "release pipeline"),
    "monitoring": ("prometheus", "latency", "throughput", "error rates", "monitor model performance"),
    "drift_detection": ("drift detection", "data drifts", "concept drift", "distribution shift"),
    "model_deployment": ("production-grade", "production ready", "deployed", "serving", "highly available"),
    "data_pipelines": ("streaming pipeline", "data pipeline", "data ingestion", "preprocessing", "cleaning"),
    "algorithms": ("algorithmic", "optimized logic", "computational problems"),
    "data_structures": ("data structures & algorithms", "trees", "graphs", "leetcode"),
    "deep_learning": ("neural network", "neural networks", "deep learning"),
    "graphql": ("graphql",),
    "rag": ("rag", "retrieval augmented generation", "reranking", "dense retrieval"),
    "model_evaluation": ("model evaluation", "evaluation framework", "evaluation platform", "slice diagnostics"),
}


@dataclass
class AnalysisOutcome:
    ats_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    suggestions: str
    summary: str
    strengths: list[str]
    risks: list[str]
    keyword_coverage: float
    section_score: float
    impact_score: float
    formatting_score: float

    def as_db_payload(self) -> dict[str, str | float]:
        return {
            "ats_score": float(self.ats_score),
            "matched_skills": json.dumps(self.matched_skills),
            "missing_skills": json.dumps(self.missing_skills),
            "suggestions": self.suggestions,
            "summary": self.summary,
            "strengths": json.dumps(self.strengths),
            "risks": json.dumps(self.risks),
            "keyword_coverage": self.keyword_coverage,
            "section_score": self.section_score,
            "impact_score": self.impact_score,
            "formatting_score": self.formatting_score,
        }


def get_skill_definitions(labels: list[str]) -> list[SkillDefinition]:
    definitions: list[SkillDefinition] = []
    for label in labels:
        for skill in SKILL_CATALOG:
            if skill.label == label:
                definitions.append(skill)
                break
    return definitions


def categorize_skill_groups(labels: list[str], role: str | None, kind: str) -> list[dict[str, object]]:
    if not labels:
        return []

    definitions = get_skill_definitions(labels)
    role_name = (role or "").lower()
    bucket_map = get_role_bucket_map(role_name)
    grouped: dict[str, list[str]] = {}

    for definition in definitions:
        bucket = bucket_map.get(definition.category, definition.category)
        grouped.setdefault(bucket, []).append(definition.label)

    ordered_groups: list[dict[str, object]] = []
    for heading in bucket_order(role_name, kind):
        items = grouped.pop(heading, None)
        if items:
            ordered_groups.append(
                {
                    "title": heading,
                    "items": sorted(items),
                }
            )

    for heading in sorted(grouped):
        ordered_groups.append(
            {
                "title": heading,
                "items": sorted(grouped[heading]),
            }
        )

    return ordered_groups


def build_audit_sections(
    role: str | None,
    ats_score: int,
    matched: list[str],
    missing: list[str],
    strengths: list[str],
    risks: list[str],
    breakdown: dict[str, float],
    suggestions: str,
) -> dict[str, object]:
    quick_wins = build_quick_wins(role, missing, matched)
    verdict = build_final_verdict(role, ats_score, missing, matched)
    score_explanations = build_score_explanations(breakdown, matched, missing)
    return {
        "matchedGroups": categorize_skill_groups(matched, role, "matched"),
        "missingGroups": categorize_skill_groups(missing, role, "missing"),
        "quickWins": quick_wins,
        "finalVerdict": verdict,
        "scoreExplanations": score_explanations,
        "atsRiskLevel": risk_level_from_score(ats_score, missing),
        "summaryHeadline": summary_headline(ats_score),
        "priorityGapHeadline": priority_gap_headline(role, missing),
        "strengthHighlights": strengths[:3],
        "riskHighlights": risks[:3],
        "suggestionBullets": split_sentences(suggestions),
    }


def analyze_resume(resume_text: str, job_description: str, job_role: str | None) -> AnalysisOutcome:
    resume_normalized = normalize_text(resume_text)
    job_normalized = normalize_text(job_description)
    role_normalized = normalize_text(job_role or "")
    profile = detect_role_profile(role_normalized, job_normalized)

    resume_scores = extract_skill_scores(resume_normalized)
    job_scores = extract_skill_scores(job_normalized)
    prioritized_job_skills = prioritize_job_skills(job_scores, profile, limit=12)

    matched_keys = [key for key in prioritized_job_skills if resume_scores.get(key, 0) > 0]
    missing_keys = [key for key in prioritized_job_skills if resume_scores.get(key, 0) == 0]

    matched = [SKILL_LOOKUP[key].label for key in matched_keys]
    missing = [SKILL_LOOKUP[key].label for key in missing_keys]

    keyword_coverage = score_keyword_coverage(
        matched_keys,
        prioritized_job_skills,
        resume_normalized,
        job_normalized,
        ROLE_PROFILES.get(profile or "", {}),
    )
    section_score = score_sections(resume_text)
    impact_score = score_impact(resume_text)
    formatting_score = score_formatting(resume_text)

    ats_score = round(
        min(
            100,
            keyword_coverage * 0.58
            + section_score * 0.14
            + impact_score * 0.16
            + formatting_score * 0.12,
        )
    )

    strengths = build_strengths(matched, section_score, impact_score, formatting_score, profile)
    risks = build_risks(missing, section_score, impact_score, formatting_score, profile)
    suggestions = build_suggestions(missing, resume_text, matched, profile)
    summary = build_summary(ats_score, matched, missing, job_role, profile)

    return AnalysisOutcome(
        ats_score=ats_score,
        matched_skills=matched[:10],
        missing_skills=missing[:6],
        suggestions=suggestions,
        summary=summary,
        strengths=strengths[:5],
        risks=risks[:5],
        keyword_coverage=round(keyword_coverage, 2),
        section_score=round(section_score, 2),
        impact_score=round(impact_score, 2),
        formatting_score=round(formatting_score, 2),
    )


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip().lower()


def detect_role_profile(role_text: str, job_text: str) -> str | None:
    explicit = normalize_role_alias(role_text)
    if explicit:
        return explicit

    combined = f"{role_text} {job_text}".strip()
    inferred = infer_role_from_text(combined)
    if inferred:
        return inferred

    if "backend" in combined:
        return "backend developer"
    if "frontend" in combined:
        return "frontend developer"
    if "full stack" in combined:
        return "full stack developer"
    if "data analyst" in combined or "business analyst" in combined:
        return "data analyst"
    if "ml engineer" in combined or "machine learning engineer" in combined or "ai engineer" in combined:
        return "ai/ml engineer"
    if "devops" in combined or "site reliability" in combined or "sre" in combined:
        return "devops engineer"
    if "software engineer" in combined:
        return "software engineer"
    return None


def normalize_role_alias(role_text: str) -> str | None:
    normalized = normalize_text(role_text)
    if not normalized:
        return None

    for role_name, aliases in ROLE_ALIASES.items():
        if normalized == role_name:
            return role_name
        if normalized in aliases:
            return role_name
    return None


def infer_role_from_text(text: str) -> str | None:
    scored_matches: list[tuple[int, int, str]] = []
    for role_name, aliases in ROLE_ALIASES.items():
        for alias in aliases:
            if alias in text:
                scored_matches.append((len(alias.split()), len(alias), role_name))
                break
    if not scored_matches:
        return None
    scored_matches.sort(reverse=True)
    return scored_matches[0][2]


def extract_skill_scores(text: str) -> dict[str, float]:
    scores: dict[str, float] = {}
    for skill in SKILL_CATALOG:
        score = 0.0
        for alias in skill.aliases:
            pattern = r"\b" + re.escape(alias).replace(r"\ ", r"\s+") + r"\b"
            matches = re.findall(pattern, text, re.I)
            if matches:
                score += len(matches) * (1.0 + min(len(alias.split()) * 0.15, 0.6))
        for signal in SEMANTIC_SIGNAL_MAP.get(skill.key, ()):
            if signal in text:
                score += 0.8
        if score > 0:
            scores[skill.key] = round(score, 2)
    return scores


def prioritize_job_skills(job_scores: dict[str, float], profile: str | None, limit: int = 10) -> list[str]:
    if not job_scores and profile:
        weighted = sorted(ROLE_PROFILES[profile].items(), key=lambda item: (-item[1], SKILL_LOOKUP[item[0]].label))
        return [key for key, _ in weighted[:limit]]

    weighted: list[tuple[str, float]] = []
    profile_weights = ROLE_PROFILES.get(profile or "", {})
    for key, score in job_scores.items():
        weight = profile_weights.get(key, 0)
        weighted.append((key, min(score, 2.5) * 4 + weight * 6))

    weighted.sort(key=lambda item: (-item[1], SKILL_LOOKUP[item[0]].label))
    prioritized = [key for key, _ in weighted if profile_weights.get(key, 0) > 0]
    if len(prioritized) < limit:
        for key, _ in weighted:
            if key not in prioritized:
                prioritized.append(key)
            if len(prioritized) >= limit:
                break
    return prioritized[:limit]


def score_keyword_coverage(
    matched_keys: list[str],
    jd_keys: list[str],
    resume_text: str,
    job_text: str,
    role_weights: dict[str, int],
) -> float:
    if jd_keys:
        weighted_total = sum(role_weights.get(key, 1) for key in jd_keys)
        weighted_matched = sum(role_weights.get(key, 1) for key in matched_keys)
        return min(100.0, weighted_matched / max(1, weighted_total) * 100.0)

    resume_words = set(tokenize(resume_text))
    job_words = set(tokenize(job_text))
    overlap = len(resume_words & job_words)
    total = max(1, len(job_words))
    return min(100.0, overlap / total * 100.0)


def score_sections(resume_text: str) -> float:
    found = 0
    for pattern in SECTION_PATTERNS.values():
        if pattern.search(resume_text):
            found += 1
    return found / len(SECTION_PATTERNS) * 100.0


def score_impact(resume_text: str) -> float:
    bullets = re.findall(r"^[\-\u2022*].+$", resume_text, re.M)
    bullet_count = len(bullets)
    action_hits = sum(1 for verb in ACTION_VERBS if re.search(rf"\b{verb}\b", resume_text, re.I))
    quantified_hits = len(re.findall(r"\b\d+%|\b\d+\+?|\$\d+", resume_text))
    weak_hits = sum(1 for pattern in WEAK_PATTERNS if pattern.search(resume_text))

    raw = 30 + min(25, bullet_count * 2.5) + min(30, action_hits * 4) + min(25, quantified_hits * 2) - min(20, weak_hits * 4)
    return max(0.0, min(100.0, raw))


def score_formatting(resume_text: str) -> float:
    lines = [line.strip() for line in resume_text.splitlines()]
    non_empty = [line for line in lines if line]
    if not non_empty:
        return 0.0

    avg_line_length = sum(len(line) for line in non_empty) / len(non_empty)
    too_long_penalty = 20 if avg_line_length > 140 else 0
    all_caps_penalty = min(20, sum(1 for line in non_empty if len(line) > 8 and line.isupper()) * 4)
    dense_penalty = 20 if len(non_empty) < 8 else 0
    return max(0.0, 100.0 - too_long_penalty - all_caps_penalty - dense_penalty)


def compute_semantic_fit(resume_text: str, job_description: str) -> float:
    resume_tokens = set(tokenize(resume_text))
    job_tokens = set(tokenize(job_description))
    if not job_tokens:
        return 0.0
    overlap = len(resume_tokens & job_tokens)
    lexical = overlap / max(1, len(job_tokens)) * 100.0
    semantic_bonus = 0.0
    boosted_pairs = [
        ("containerization", "docker"),
        ("deployment", "model"),
        ("monitor", "performance"),
        ("data", "pipeline"),
        ("algorithm", "design"),
        ("machine", "learning"),
    ]
    lowered_resume = resume_text.lower()
    lowered_jd = job_description.lower()
    for left, right in boosted_pairs:
        if left in lowered_resume and right in lowered_jd:
            semantic_bonus += 3.5
    return min(100.0, lexical + semantic_bonus)


def build_section_insights(resume_text: str, job_description: str) -> list[dict[str, object]]:
    lowered = resume_text.lower()
    jd_lowered = job_description.lower()
    sections = [
        (
            "Summary",
            extract_section_block(lowered, "summary", ("technical skills", "skills", "projects", "experience")),
            "Focuses on role targeting and first-impression clarity.",
        ),
        (
            "Skills",
            extract_section_block(lowered, "technical skills", ("projects", "experience", "achievements")),
            "This is the highest-leverage ATS section for explicit keyword matching.",
        ),
        (
            "Projects",
            extract_section_block(lowered, "projects", ("achievements", "education", "certifications")),
            "Projects are where production evidence and ownership become credible.",
        ),
        (
            "Experience Signals",
            lowered,
            "Measures business impact, metrics, and delivery language across the document.",
        ),
    ]
    insights: list[dict[str, object]] = []
    for title, block, commentary in sections:
        score = section_match_score(block, jd_lowered)
        highlights = section_highlights(block)
        insights.append(
            {
                "title": title,
                "score": score,
                "commentary": commentary,
                "highlights": highlights,
            }
        )
    return insights


def extract_section_block(text: str, start_keyword: str, end_keywords: tuple[str, ...]) -> str:
    start = text.find(start_keyword)
    if start == -1:
        return ""
    end_positions = [text.find(keyword, start + len(start_keyword)) for keyword in end_keywords if text.find(keyword, start + len(start_keyword)) != -1]
    end = min(end_positions) if end_positions else len(text)
    return text[start:end]


def section_match_score(section_text: str, job_description: str) -> int:
    if not section_text:
        return 25
    section_tokens = set(tokenize(section_text))
    job_tokens = set(tokenize(job_description))
    overlap = len(section_tokens & job_tokens)
    raw = min(100, 35 + overlap * 4)
    return max(25, raw)


def section_highlights(section_text: str) -> list[str]:
    if not section_text:
        return ["Section is missing or too thin to contribute strongly to ATS screening."]
    highlights: list[str] = []
    if re.search(r"\bpython\b", section_text):
        highlights.append("Python is clearly visible.")
    if re.search(r"\b(pytorch|tensorflow|scikit-learn|pandas)\b", section_text):
        highlights.append("Core ML frameworks are explicitly listed.")
    if re.search(r"\b\d+%|\b\d+\+?|\bp99\b", section_text):
        highlights.append("Quantified results are present.")
    if re.search(r"\b(docker|ci/cd|github actions|prometheus|kafka)\b", section_text):
        highlights.append("Production engineering signals are present.")
    if not highlights:
        highlights.append("This section could use more explicit, job-aligned keywords.")
    return highlights[:3]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9.+#/-]*", text.lower())


def build_strengths(
    matched: list[str],
    section_score: float,
    impact_score: float,
    formatting_score: float,
    profile: str | None,
) -> list[str]:
    strengths: list[str] = []
    if matched:
        strengths.append(f"The resume aligns best on core requirements such as {', '.join(matched[:4])}.")
    if profile == "ai/ml engineer" and {"Monitoring", "Drift Detection", "Model Evaluation", "RAG", "Data Pipelines", "Model Deployment"} & set(matched):
        strengths.append("Production ML depth is visible through monitoring, evaluation, and real-world ML systems evidence rather than only notebook-level work.")
    if profile and matched:
        strengths.append(f"Role targeting is visible for the {display_role_name(profile)} path rather than being fully generic.")
    if section_score >= 65:
        strengths.append("The resume structure is ATS-friendly with several standard sections clearly signposted.")
    if impact_score >= 70:
        strengths.append("Experience bullets show action and measurable delivery, which improves recruiter confidence.")
    if formatting_score >= 80:
        strengths.append("Formatting is readable and likely to parse well in automated screening systems.")
    if not strengths:
        strengths.append("The resume has a workable foundation and can improve with stronger role-specific evidence.")
    return strengths


def build_risks(
    missing: list[str],
    section_score: float,
    impact_score: float,
    formatting_score: float,
    profile: str | None,
) -> list[str]:
    risks: list[str] = []
    if missing:
        risks.append(f"Important target-role skills are not clearly evidenced, especially {', '.join(missing[:4])}.")
    if profile == "ai/ml engineer" and {"Linear Algebra", "Calculus", "Probability"} & set(missing):
        risks.append("Mathematics foundations are part of the job spec, so missing explicit math keywords can hurt ATS filtering even if the knowledge is implicit.")
    if profile and len(missing) >= 3:
        risks.append(f"The profile still looks underpowered for a {display_role_name(profile)} role unless those gaps are addressed.")
    if section_score < 50:
        risks.append("Missing standard resume sections may reduce completeness in ATS screening.")
    if impact_score < 55:
        risks.append("Bullet points read more like responsibilities than outcomes and need stronger business impact.")
    if formatting_score < 70:
        risks.append("Formatting density may make recruiter review slower and less skimmable.")
    if not risks:
        risks.append("No major fit risks stand out, but tighter tailoring would still improve competitiveness.")
    return risks


def build_suggestions(missing: list[str], resume_text: str, matched: list[str], profile: str | None) -> str:
    suggestions: list[str] = []
    if missing:
        suggestions.append(f"Prioritize adding project or experience evidence for {', '.join(missing[:4])} wherever that experience is real and defensible.")
    if len(re.findall(r"\b\d+%|\b\d+\+?|\$\d+", resume_text)) < 3:
        suggestions.append("Strengthen credibility by quantifying outcomes with delivery metrics, scale, latency, revenue, or time saved.")
    if not SECTION_PATTERNS["summary"].search(resume_text):
        suggestions.append("Add a focused professional summary that positions you for the target role in the first few lines.")
    if not SECTION_PATTERNS["projects"].search(resume_text):
        suggestions.append("Include one strong project section that proves hands-on ownership with the same tools the job asks for.")
    if matched:
        suggestions.append(f"Move experience containing {', '.join(matched[:3])} higher on the page so your strongest signals appear earlier.")
    if profile in {"backend developer", "software engineer"}:
        suggestions.append("Make architecture, API ownership, reliability, and testing impact more explicit in your bullet points.")
    if profile == "ai/ml engineer":
        suggestions.append("Differentiate model-building work from deployment work so the AI/ML depth is obvious at a glance.")
        suggestions.append("Spell out core foundations like C++, Pandas, probability, statistics, data structures, and deep learning when they are genuinely part of your background.")
    if not suggestions:
        suggestions.append("Tailor the resume more tightly to the job description and lead with the most relevant achievements.")
    return " ".join(suggestions)


def build_summary(
    ats_score: int,
    matched: list[str],
    missing: list[str],
    job_role: str | None,
    profile: str | None,
) -> str:
    role_name = job_role or (display_role_name(profile) if profile else "the target role")
    if ats_score >= 80:
        level = "strong"
    elif ats_score >= 65:
        level = "moderate"
    else:
        level = "limited"

    summary = f"This resume shows {level} alignment for {role_name}. "
    if matched:
        summary += f"The strongest evidence appears around {', '.join(matched[:4])}. "
    if missing:
        summary += f"The main gaps are {', '.join(missing[:4])}, which should be addressed with clearer proof of hands-on use."
    else:
        summary += "The key required skills are mostly covered, so improvements should focus on clarity, impact, and prioritization."
    return summary


def get_role_bucket_map(role_name: str) -> dict[str, str]:
    if "ai/ml" in role_name or "machine learning" in role_name or "ai engineer" in role_name:
        return {
            "Programming": "Core ML & Engineering",
            "AI/ML": "Core ML & Engineering",
            "Data": "Core ML & Engineering",
            "Backend": "MLOps / Production Skills",
            "Cloud": "Deployment / Systems",
            "Data Engineering": "Big Data & Pipelines",
            "Tooling": "MLOps / Production Skills",
            "Architecture": "Production Systems Design",
            "Quality": "MLOps / Production Skills",
            "Analytics": "Analytics & Reporting",
        }
    if "backend" in role_name:
        return {
            "Programming": "Core Backend",
            "Backend": "Core Backend",
            "Data": "Data & Storage",
            "Cloud": "Cloud & Infrastructure",
            "Architecture": "Architecture",
            "Tooling": "Dev Workflow",
            "Quality": "Testing & Reliability",
            "Data Engineering": "Streaming & Data",
        }
    return {
        "Programming": "Core Engineering",
        "Backend": "Core Engineering",
        "Frontend": "Product Engineering",
        "Data": "Data & Analytics",
        "Cloud": "Cloud & Infrastructure",
        "Tooling": "Tooling",
        "Architecture": "Architecture",
        "Quality": "Quality",
        "AI/ML": "AI & ML",
        "Data Engineering": "Data Engineering",
        "Analytics": "Analytics",
    }


def bucket_order(role_name: str, kind: str) -> list[str]:
    if "ai/ml" in role_name or "machine learning" in role_name or "ai engineer" in role_name:
        order = [
            "Core ML & Engineering",
            "MLOps / Production Skills",
            "Deployment / Systems",
            "Big Data & Pipelines",
            "Production Systems Design",
            "Analytics & Reporting",
        ]
    elif "backend" in role_name:
        order = [
            "Core Backend",
            "Data & Storage",
            "Cloud & Infrastructure",
            "Architecture",
            "Testing & Reliability",
            "Dev Workflow",
            "Streaming & Data",
        ]
    else:
        order = [
            "Core Engineering",
            "Product Engineering",
            "Data & Analytics",
            "Cloud & Infrastructure",
            "Architecture",
            "AI & ML",
            "Tooling",
            "Quality",
            "Data Engineering",
            "Analytics",
        ]
    return order


def build_quick_wins(role: str | None, missing: list[str], matched: list[str]) -> list[str]:
    wins: list[str] = []
    if missing:
        wins.append(f"Add explicit keywords for {', '.join(missing[:4])} in the skills or projects section where you have genuine exposure.")
    if role and "ai/ml" in role.lower():
        wins.append("State ML foundations explicitly with terms like supervised learning, deep learning, NLP, model evaluation, and deployment.")
        wins.append("Surface production ML signals early by highlighting inference APIs, monitoring, model evaluation, and pipeline ownership.")
    if role and "backend" in role.lower():
        wins.append("Make API ownership, architecture decisions, testing, and reliability metrics more obvious in recent experience bullets.")
    if matched:
        wins.append(f"Move the strongest evidence for {', '.join(matched[:3])} closer to the top third of the resume.")
    wins.append("Keep metrics attached to technical work so ATS keywords also look credible to human reviewers.")
    return wins[:4]


def build_final_verdict(role: str | None, ats_score: int, missing: list[str], matched: list[str]) -> str:
    role_name = role or "this target role"
    if ats_score >= 85:
        tone = "This is a strong profile"
    elif ats_score >= 70:
        tone = "This is a competitive profile"
    elif ats_score >= 55:
        tone = "This profile has good potential"
    else:
        tone = "This profile is currently under-signaled"
    if missing and ats_score >= 85 and len(missing) <= 2:
        return f"{tone} for {role_name}. The main remaining lift is to make keywords like {', '.join(missing[:3])} more explicit rather than to fix major capability gaps."
    if missing:
        return f"{tone} for {role_name}, but it will likely underperform in ATS screening until missing keywords like {', '.join(missing[:3])} are made explicit."
    return f"{tone} for {role_name}, and the main remaining gains will come from sharper prioritization and stronger measurable impact."


def build_score_explanations(breakdown: dict[str, float], matched: list[str], missing: list[str]) -> list[dict[str, object]]:
    return [
        {
            "title": "Keyword Coverage",
            "score": round(breakdown.get("keywordCoverage", 0)),
            "commentary": (
                f"Strongest visible keywords include {', '.join(matched[:4])}."
                if matched
                else "Keyword coverage is still weak and needs clearer alignment with the job description."
            ),
        },
        {
            "title": "Semantic Fit",
            "score": round(breakdown.get("semanticFit", 0)),
            "commentary": "Estimates how strongly the resume’s language and project signals align with the job description beyond direct keyword repetition.",
        },
        {
            "title": "Section Quality",
            "score": round(breakdown.get("sectionScore", 0)),
            "commentary": "Resume sectioning looks ATS-friendly, but clearer labeling and ordering can still improve skimmability.",
        },
        {
            "title": "Impact Score",
            "score": round(breakdown.get("impactScore", 0)),
            "commentary": "Quantified outcomes and ownership signals are what make this score move upward the fastest.",
        },
        {
            "title": "Formatting",
            "score": round(breakdown.get("formattingScore", 0)),
            "commentary": (
                "Formatting appears readable for both ATS systems and recruiters."
                if breakdown.get("formattingScore", 0) >= 80
                else "Formatting should be simplified to improve readability and parser reliability."
            ),
        },
    ]


def risk_level_from_score(ats_score: int, missing: list[str]) -> str:
    if ats_score >= 85 and len(missing) <= 1:
        return "Low ATS Risk"
    if ats_score >= 65 and len(missing) <= 3:
        return "Moderate ATS Risk"
    return "High ATS Risk"


def summary_headline(ats_score: int) -> str:
    if ats_score >= 85:
        return "Strong Alignment"
    if ats_score >= 70:
        return "Competitive Alignment"
    if ats_score >= 55:
        return "Partial Alignment"
    return "Needs Stronger Targeting"


def priority_gap_headline(role: str | None, missing: list[str]) -> str:
    if not missing:
        return "No major target-role gaps detected"
    role_name = role or "the role"
    return f"Highest-priority gaps for {role_name}: {', '.join(missing[:3])}"


def split_sentences(text: str) -> list[str]:
    if not text:
        return []
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def display_role_name(role_name: str | None) -> str:
    if not role_name:
        return "Target Role"
    mapping = {
        "ai/ml engineer": "AI/ML Engineer",
        "backend developer": "Backend Developer",
        "frontend developer": "Frontend Developer",
        "full stack developer": "Full Stack Developer",
        "software engineer": "Software Engineer",
        "data analyst": "Data Analyst",
        "devops engineer": "DevOps Engineer",
    }
    normalized = role_name.lower()
    return mapping.get(normalized, role_name.title())
