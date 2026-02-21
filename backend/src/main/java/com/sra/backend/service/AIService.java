package com.sra.backend.service;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;   // <-- add this import
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.util.List;

/** Uses OpenAI for suggestions with graceful fallback. */
@Service
public class AIService {
    private static final Logger log = LogManager.getLogger(AIService.class);
    private final AIClientAdapter adapter;

    @Autowired  // <-- tell Spring to use THIS constructor
    public AIService(@Value("${OPENAI_API_KEY:}") String apiKey){
        this.adapter = (apiKey==null || apiKey.isBlank()) ? null : new OpenAIClientAdapter(apiKey);
        if(this.adapter == null) log.warn("OPENAI_API_KEY not set; using fallback suggestions.");
        else log.info("OPENAI_API_KEY detected. Using OpenAIClientAdapter.");
    }

    // For tests (not used by Spring context)
    public AIService(AIClientAdapter testAdapter){ this.adapter = testAdapter; }

    public static class Advice {
        public final String suggestions; public final String summary;
        public Advice(String s, String m){ this.suggestions=s; this.summary=m; }
    }

    public Advice advise(List<String> missingSkills, String jobRole){
        try{
            String missing = (missingSkills==null || missingSkills.isEmpty()) ? "None" : String.join(", ", missingSkills);
            String prompt = "Analyze missing skills for role \"" + jobRole + "\": " + missing + ". 1) Suggest 2-5 actionable improvements (courses/certs/sections to add). 2) One-sentence summary. Format: Suggestions: ...\nSummary: ...";
            String text;
            if(adapter == null){
                text = "Suggestions: Add or strengthen: " + missing + ".\nMirror JD keywords; quantify outcomes.\nSummary: Solid baseline for " + jobRole + "; address gaps for better ATS alignment.";
            } else {
                text = adapter.generateAdvice(prompt);
            }
            String suggestions = text, summary = "";
            int idx = text.toLowerCase().indexOf("summary:");
            if(idx >= 0){
                suggestions = text.substring(0, idx).replaceFirst("(?i)^suggestions:\\s*", "").trim();
                summary = text.substring(idx).replaceFirst("(?i)^summary:\\s*", "").trim();
            }
            if(summary.isBlank()) summary = "Good fit for " + jobRole + "; highlight missing skills to improve alignment.";
            log.info("AI suggestions generated ({} chars).", text.length());
            return new Advice(suggestions, summary);
        } catch(Exception e){
            log.error("AI advise failed", e);
            return new Advice("- Address gaps listed.\n- Quantify achievements.\n- Mirror JD terms.", "Reasonable fit; address gaps for improved ATS score.");
        }
    }
}
