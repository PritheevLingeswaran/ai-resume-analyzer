from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UploadResponse(BaseModel):
    resumeId: int
    fileName: str
    extractedText: str
    createdAt: datetime


class AnalyzeRequest(BaseModel):
    resumeText: str = Field(min_length=20)
    jobDescription: str = Field(min_length=20)
    jobRole: str | None = Field(default=None, max_length=150)


class AnalysisBreakdown(BaseModel):
    keywordCoverage: float
    sectionScore: float
    impactScore: float
    formattingScore: float
    semanticFit: float


class SkillGroup(BaseModel):
    title: str
    items: list[str]


class ScoreExplanation(BaseModel):
    title: str
    score: int
    commentary: str


class AuditSection(BaseModel):
    matchedGroups: list[SkillGroup]
    missingGroups: list[SkillGroup]
    quickWins: list[str]
    finalVerdict: str
    scoreExplanations: list[ScoreExplanation]
    atsRiskLevel: str
    summaryHeadline: str
    priorityGapHeadline: str
    strengthHighlights: list[str]
    riskHighlights: list[str]
    suggestionBullets: list[str]


class SectionInsight(BaseModel):
    title: str
    score: int
    commentary: str
    highlights: list[str]


class ReportMeta(BaseModel):
    shareUrl: str
    generatedForRole: str | None
    createdAt: datetime


class RewriteSuggestion(BaseModel):
    title: str
    before: str
    after: str
    rationale: str


class RewriteResponse(BaseModel):
    role: str | None
    summaryRewrite: str
    headlineOptions: list[str]
    suggestions: list[RewriteSuggestion]


class ReportListItem(BaseModel):
    id: int
    role: str | None
    ats_score: int
    summaryHeadline: str
    createdAt: datetime
    shareUrl: str


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resumeId: int
    jobId: int
    ats_score: int
    matchedSkills: list[str]
    missingSkills: list[str]
    suggestions: str
    summary: str
    strengths: list[str]
    risks: list[str]
    breakdown: AnalysisBreakdown
    audit: AuditSection
    sections: list[SectionInsight]
    meta: ReportMeta
    timestamp: datetime


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
