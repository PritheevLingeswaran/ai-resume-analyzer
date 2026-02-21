package com.sra.backend.service;

import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

public class NLPServiceTest {
    @Test
    void tokenization_and_keywords(){
        NLPService nlp = new NLPService();
        String text = "Experienced in Java Spring Boot, REST APIs, AWS, and Docker.";
        String[] toks = nlp.tokenize(text);
        assertTrue(toks.length >= 5);
        List<String> kw = nlp.extractKeywords(text);
        assertTrue(kw.contains("java"));
        assertTrue(kw.contains("aws"));
    }
}
