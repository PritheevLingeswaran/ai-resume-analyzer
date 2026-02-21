package com.sra.backend.service;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.tika.Tika;
import org.springframework.stereotype.Service;
import java.io.InputStream;

/** Uses Apache Tika to extract text from uploaded resume files. */
@Service
public class ResumeService {
    private static final Logger log = LogManager.getLogger(ResumeService.class);
    private final Tika tika = new Tika();

    public String extractText(InputStream in){
        try{
            String text = tika.parseToString(in);
            log.info("Tika extracted {} chars", text==null?0:text.length());
            return text;
        } catch(Exception e){
            log.error("Tika extraction failed", e);
            throw new RuntimeException("Extraction failed", e);
        }
    }
}
