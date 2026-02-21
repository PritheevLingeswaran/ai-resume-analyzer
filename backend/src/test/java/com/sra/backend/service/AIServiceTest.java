package com.sra.backend.service;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AIServiceTest {
    @Test
    void adapter_and_fallback(){
        AIService svc1 = new AIService((AIClientAdapter) prompt -> "Suggestions: Learn Docker\nSummary: Great fit");
        var a1 = svc1.advise(java.util.List.of("docker"), "Backend Developer");
        assertTrue(a1.suggestions.toLowerCase().contains("docker"));
        assertTrue(a1.summary.toLowerCase().contains("fit"));

        AIService svc2 = new AIService((AIClientAdapter)null);
        var a2 = svc2.advise(java.util.List.of("kafka"), "Backend Developer");
        assertNotNull(a2.suggestions);
        assertNotNull(a2.summary);
    }
}
