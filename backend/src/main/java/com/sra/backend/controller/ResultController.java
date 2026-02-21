package com.sra.backend.controller;

import com.sra.backend.dao.ResultDAO;
import com.sra.backend.model.AnalysisResult;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.sql.DataSource;
import java.util.Map;

@CrossOrigin(origins = "*")
@RestController @RequestMapping("/api")
public class ResultController {
    private static final Logger log = LogManager.getLogger(ResultController.class);
    private final ResultDAO dao;

    public ResultController(DataSource ds){
        this.dao = new ResultDAO(ds);
    }

    @GetMapping("/result/{id}")
    public ResponseEntity<?> getById(@PathVariable long id){
        try{
            AnalysisResult r = dao.findById(id);
            if(r == null) return ResponseEntity.notFound().build();
            return ResponseEntity.ok(Map.of(
                "id", r.getId(),
                "resumeId", r.getResumeId(),
                "jobId", r.getJobId(),
                "ats_score", r.getAtsScore(),
                "matchedSkills", r.getMatchedSkills(),
                "missingSkills", r.getMissingSkills(),
                "suggestions", r.getSuggestions(),
                "timestamp", r.getTimestamp()
            ));
        }catch(Exception e){
            log.error("Failed to fetch result {}", id, e);
            return ResponseEntity.internalServerError().body(Map.of("error","Failed to fetch analysis result."));
        }
    }
}
