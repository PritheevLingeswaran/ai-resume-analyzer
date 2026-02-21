package com.sra.backend.model;
public class Resume {
    private Long id; private String fileName; private String filePath; private String extractedText;
    public Resume(){}
    public Resume(Long id, String fileName, String filePath, String extractedText){ this.id=id; this.fileName=fileName; this.filePath=filePath; this.extractedText=extractedText; }
    public Resume(String fileName, String filePath, String extractedText){ this(null,fileName,filePath,extractedText); }
    public Long getId(){ return id; } public void setId(Long id){ this.id=id; }
    public String getFileName(){ return fileName; } public void setFileName(String s){ this.fileName=s; }
    public String getFilePath(){ return filePath; } public void setFilePath(String s){ this.filePath=s; }
    public String getExtractedText(){ return extractedText; } public void setExtractedText(String s){ this.extractedText=s; }
}
