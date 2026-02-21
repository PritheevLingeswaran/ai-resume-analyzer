package com.sra.backend.controller;

import com.sra.backend.dao.ResultDAO;
import com.sra.backend.model.AnalysisResult;
import com.sra.backend.model.api.AnalysisPayload;
import com.sra.backend.service.AnalysisService;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Map;

@CrossOrigin(origins = "*")
@RestController @RequestMapping("/api")
public class AnalysisController {
    private static final Logger log = LogManager.getLogger(AnalysisController.class);
    private final AnalysisService svc;
    private final ResultDAO resultDAO;

    public AnalysisController(AnalysisService svc, DataSource ds){ this.svc = svc; this.resultDAO = new ResultDAO(ds); }

    @PostMapping(path="/analyze", consumes=MediaType.APPLICATION_JSON_VALUE, produces=MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> analyze(@RequestBody Map<String,String> payload){
        String resume = payload.getOrDefault("resumeText","");
        String jd = payload.getOrDefault("jobDescription","");
        String role = payload.getOrDefault("jobRole","the role");

        if(resume==null || resume.isBlank() || jd==null || jd.isBlank()){
            log.warn("Bad request: empty resume or JD");
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(Map.of("error","Resume text or job description cannot be empty."));
        }
        try{
            AnalysisPayload p = svc.analyze(resume, jd, role);

            // Persist a record (optional resume/job ids; using 0 as placeholder if unknown)
            AnalysisResult rec = new AnalysisResult(0L, 0L, p.getAtsScore(), p.getMatchedSkills().toString(), p.getMissingSkills().toString(), p.getSuggestions());
            resultDAO.insertResult(rec);

            Map<String,Object> out = new HashMap<>();
            out.put("ats_score", p.getAtsScore());
            out.put("matchedSkills", p.getMatchedSkills());
            out.put("missingSkills", p.getMissingSkills());
            out.put("suggestions", p.getSuggestions());
            out.put("summary", p.getSummary());
            out.put("resultId", rec.getId());
            return ResponseEntity.ok(out);
        }catch(Exception e){
            log.error("Analyze failed", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of("error","Analysis failed."));
        }
    }
}
