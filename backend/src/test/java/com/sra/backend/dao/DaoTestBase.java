package com.sra.backend.dao;

import org.junit.jupiter.api.*;
import org.sqlite.SQLiteDataSource;

import javax.sql.DataSource;
import java.io.File;
import java.sql.Connection;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class DaoTestBase {
    protected DataSource ds;

    @BeforeAll
    void setup() throws Exception {
        File dir = new File("target/test-db"); dir.mkdirs();
        File db = new File(dir, "sra-test.db");
        SQLiteDataSource s = new SQLiteDataSource();
        s.setUrl("jdbc:sqlite:" + db.getPath());
        this.ds = s;
        try(Connection c = ds.getConnection()){
            DatabaseUtil.createSchemaIfNeeded(ds);
        }
    }
}
