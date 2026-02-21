package com.sra.backend.model.api;

import java.util.List;

public class AnalysisPayload {
    private int atsScore;
    private java.util.List<String> matchedSkills;
    private java.util.List<String> missingSkills;
    private String suggestions;
    private String summary;

    public AnalysisPayload(){}
    public AnalysisPayload(int atsScore, java.util.List<String> matchedSkills, java.util.List<String> missingSkills, String suggestions, String summary){
        this.atsScore=atsScore; this.matchedSkills=matchedSkills; this.missingSkills=missingSkills; this.suggestions=suggestions; this.summary=summary;
    }
    public int getAtsScore(){ return atsScore; } public void setAtsScore(int x){ this.atsScore=x; }
    public java.util.List<String> getMatchedSkills(){ return matchedSkills; } public void setMatchedSkills(java.util.List<String> x){ this.matchedSkills=x; }
    public java.util.List<String> getMissingSkills(){ return missingSkills; } public void setMissingSkills(java.util.List<String> x){ this.missingSkills=x; }
    public String getSuggestions(){ return suggestions; } public void setSuggestions(String s){ this.suggestions=s; }
    public String getSummary(){ return summary; } public void setSummary(String s){ this.summary=s; }
}
