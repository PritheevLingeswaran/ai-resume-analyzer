package com.sra.backend.service;

import com.sra.backend.model.api.AnalysisPayload;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AnalysisServiceTest {

    @Test
    void ats_and_sets(){
        NLPService nlp = new NLPService();
        AIService ai = new AIService((AIClientAdapter) prompt -> "Suggestions: Add Kafka\nSummary: Good baseline");
        AnalysisService svc = new AnalysisService(nlp, ai);

        AnalysisPayload r = svc.analyze("Java Spring Boot Docker AWS", "We use Java, Spring, Kafka, AWS", "Backend Developer");
        assertTrue(r.getAtsScore() >= 25 && r.getAtsScore() <= 100);
        assertTrue(r.getMatchedSkills().contains("java"));
        assertTrue(r.getMissingSkills().contains("kafka"));
    }

    @Test
    void rejects_empty(){
        NLPService nlp = new NLPService();
        AIService ai = new AIService((AIClientAdapter) prompt -> "Suggestions: -\nSummary: -");
        AnalysisService svc = new AnalysisService(nlp, ai);
        assertThrows(IllegalArgumentException.class, () -> svc.analyze("", "x", "Role"));
        assertThrows(IllegalArgumentException.class, () -> svc.analyze("x", "", "Role"));
    }
}
