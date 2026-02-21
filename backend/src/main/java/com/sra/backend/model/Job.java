package com.sra.backend.model;
public class Job {
    private Long id; private String jobTitle; private String descriptionText;
    public Job(){} public Job(Long id, String jobTitle, String descriptionText){ this.id=id; this.jobTitle=jobTitle; this.descriptionText=descriptionText; }
    public Job(String jobTitle, String descriptionText){ this(null, jobTitle, descriptionText); }
    public Long getId(){ return id; } public void setId(Long id){ this.id=id; }
    public String getJobTitle(){ return jobTitle; } public void setJobTitle(String s){ this.jobTitle=s; }
    public String getDescriptionText(){ return descriptionText; } public void setDescriptionText(String s){ this.descriptionText=s; }
}
