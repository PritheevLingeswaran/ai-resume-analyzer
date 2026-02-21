package com.sra.backend.dao;

import com.sra.backend.model.AnalysisResult;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ResultDAOTest extends DaoTestBase {
    @Test
    void insert_and_find(){
        ResultDAO dao = new ResultDAO(ds);
        AnalysisResult ar = new AnalysisResult(1L,1L,80,"[java,spring]","[kafka]","Add Kafka");
        assertTrue(dao.insertResult(ar));
        assertNotNull(dao.findById(ar.getId()));
    }
}
