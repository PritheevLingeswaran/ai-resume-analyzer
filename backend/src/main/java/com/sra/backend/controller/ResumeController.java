package com.sra.backend.controller;

import com.sra.backend.dao.ResumeDAO;
import com.sra.backend.model.Resume;
import com.sra.backend.service.ResumeService;
import com.sra.backend.util.FileValidator;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.sql.DataSource;
import java.io.InputStream;
import java.util.Map;

@CrossOrigin(origins = "*")
@RestController @RequestMapping("/api")
public class ResumeController {
    private static final Logger log = LogManager.getLogger(ResumeController.class);
    private final ResumeService resumeService; private final ResumeDAO resumeDAO;
    public ResumeController(ResumeService resumeService, javax.sql.DataSource ds){ this.resumeService=resumeService; this.resumeDAO=new ResumeDAO(ds); }

    @PostMapping(path="/upload", consumes=MediaType.MULTIPART_FORM_DATA_VALUE, produces=MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> upload(@RequestPart("file") MultipartFile file){
        try{
            if(!FileValidator.validate(file)){
                log.warn("Invalid upload: {}, size={}", file!=null?file.getOriginalFilename():"null", file!=null?file.getSize():0);
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(Map.of("error","Invalid file. Only PDF/DOCX up to 5MB allowed."));
            }
            String text; try(InputStream in = file.getInputStream()){ text = resumeService.extractText(in); }
            Resume r = new Resume(null, file.getOriginalFilename(), null, text);
            boolean ok = resumeDAO.insertResume(r);
            log.info("Resume uploaded: {}", file.getOriginalFilename());
            return ResponseEntity.ok(Map.of("fileName", file.getOriginalFilename(), "extractedText", text, "resumeId", r.getId()));
        }catch(Exception e){
            log.error("Upload failed", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of("error","Upload or extraction failed."));
        }
    }
}
