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
    timestamp: datetime


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
