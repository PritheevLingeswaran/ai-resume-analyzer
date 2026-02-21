package com.sra.backend.model;
public class AnalysisResult {
    private Long id; private Long resumeId; private Long jobId; private double atsScore;
    private String matchedSkills; private String missingSkills; private String suggestions; private String timestamp;
    public AnalysisResult(){}
    public AnalysisResult(Long id, Long resumeId, Long jobId, double atsScore, String matchedSkills, String missingSkills, String suggestions, String timestamp){
        this.id=id; this.resumeId=resumeId; this.jobId=jobId; this.atsScore=atsScore; this.matchedSkills=matchedSkills; this.missingSkills=missingSkills; this.suggestions=suggestions; this.timestamp=timestamp;
    }
    public AnalysisResult(Long resumeId, Long jobId, double atsScore, String matchedSkills, String missingSkills, String suggestions){
        this(null, resumeId, jobId, atsScore, matchedSkills, missingSkills, suggestions, null);
    }
    public Long getId(){ return id; } public void setId(Long id){ this.id=id; }
    public Long getResumeId(){ return resumeId; } public void setResumeId(Long id){ this.resumeId=id; }
    public Long getJobId(){ return jobId; } public void setJobId(Long id){ this.jobId=id; }
    public double getAtsScore(){ return atsScore; } public void setAtsScore(double s){ this.atsScore=s; }
    public String getMatchedSkills(){ return matchedSkills; } public void setMatchedSkills(String s){ this.matchedSkills=s; }
    public String getMissingSkills(){ return missingSkills; } public void setMissingSkills(String s){ this.missingSkills=s; }
    public String getSuggestions(){ return suggestions; } public void setSuggestions(String s){ this.suggestions=s; }
    public String getTimestamp(){ return timestamp; } public void setTimestamp(String t){ this.timestamp=t; }
}
