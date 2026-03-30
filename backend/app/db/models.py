from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(150), nullable=True)
    extracted_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    analyses: Mapped[list["AnalysisResult"]] = relationship(back_populates="resume")


class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role: Mapped[str | None] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    analyses: Mapped[list["AnalysisResult"]] = relationship(back_populates="job")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"), nullable=False, index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job_postings.id"), nullable=False, index=True)
    ats_score: Mapped[float] = mapped_column(Float, nullable=False)
    matched_skills: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    missing_skills: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    suggestions: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    strengths: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    risks: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    keyword_coverage: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    section_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    impact_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    formatting_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    resume: Mapped[Resume] = relationship(back_populates="analyses")
    job: Mapped[JobPosting] = relationship(back_populates="analyses")
