package com.sra.backend.dao;

import com.sra.backend.model.Job;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class JobDAOTest extends DaoTestBase {
    @Test
    void insert_and_list(){
        JobDAO dao = new JobDAO(ds);
        Job j = new Job("Software Engineer", "Build REST APIs");
        assertTrue(dao.insertJob(j));
        assertNotNull(j.getId());
        assertFalse(dao.fetchAllJobs().isEmpty());
    }
}
