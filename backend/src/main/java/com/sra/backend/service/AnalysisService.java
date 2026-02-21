package com.sra.backend.service;

import com.sra.backend.model.api.AnalysisPayload;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class AnalysisService {
    private static final Logger log = LogManager.getLogger(AnalysisService.class);
    private final NLPService nlp; private final AIService ai;
    public AnalysisService(NLPService nlp, AIService ai){ this.nlp=nlp; this.ai=ai; }

    public AnalysisPayload analyze(String resumeText, String jobText, String jobRole){
        if(resumeText==null || resumeText.isBlank() || jobText==null || jobText.isBlank()){
            throw new IllegalArgumentException("Resume text or job description cannot be empty.");
        }
        List<String> resume = nlp.extractKeywords(resumeText);
        List<String> jd = nlp.extractKeywords(jobText);
        log.info("Extracted keywords: resume={}, jd={}", resume.size(), jd.size());

        Set<String> rset = new LinkedHashSet<>(resume);
        Set<String> jset = new LinkedHashSet<>(jd);
        Set<String> matched = new TreeSet<>(); for(String k: rset) if(jset.contains(k)) matched.add(k);
        Set<String> missing = new TreeSet<>(jset); missing.removeAll(rset);

        int ats = jset.isEmpty()? 0 : Math.round((matched.size()*100f)/jset.size());
        log.info("ATS score: {}", ats);

        AIService.Advice advice = ai.advise(new ArrayList<>(missing), jobRole==null? "the role" : jobRole);

        return new AnalysisPayload(ats, new ArrayList<>(matched), new ArrayList<>(missing), advice.suggestions, advice.summary);
    }
}
