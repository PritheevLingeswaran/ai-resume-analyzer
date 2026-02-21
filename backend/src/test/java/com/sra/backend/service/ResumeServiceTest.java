package com.sra.backend.service;

import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.junit.jupiter.api.Test;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import static org.junit.jupiter.api.Assertions.*;

public class ResumeServiceTest {
    @Test
    void tika_extracts_text_from_docx() throws Exception {
        XWPFDocument doc = new XWPFDocument();
        doc.createParagraph().createRun().setText("Hello Resume from DOCX");
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        doc.write(bos); doc.close();
        ResumeService svc = new ResumeService();
        String text = svc.extractText(new ByteArrayInputStream(bos.toByteArray()));
        assertNotNull(text);
        assertTrue(text.toLowerCase().contains("hello resume"));
    }
}
