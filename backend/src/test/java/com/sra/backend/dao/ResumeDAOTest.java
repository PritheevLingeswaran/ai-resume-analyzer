package com.sra.backend.dao;

import com.sra.backend.model.Resume;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ResumeDAOTest extends DaoTestBase {
    @Test
    void insert_and_fetch(){
        ResumeDAO dao = new ResumeDAO(ds);
        Resume r = new Resume("Pritheev_Resume.pdf", "/uploads/Pritheev_Resume.pdf", "Java Developer...");
        assertTrue(dao.insertResume(r));
        assertNotNull(r.getId());
        Resume got = dao.fetchResumeById(r.getId());
        assertEquals("Pritheev_Resume.pdf", got.getFileName());
    }
}
