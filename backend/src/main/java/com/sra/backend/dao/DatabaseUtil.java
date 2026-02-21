package com.sra.backend.dao;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

public class DatabaseUtil {
    private static final Logger log = LogManager.getLogger(DatabaseUtil.class);

    public static void createSchemaIfNeeded(DataSource ds){
        try(Connection c = ds.getConnection(); Statement st = c.createStatement()){
            st.execute("PRAGMA foreign_keys=ON");
            st.executeUpdate("CREATE TABLE IF NOT EXISTS resumes (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, file_path TEXT, extracted_text TEXT)");
            st.executeUpdate("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, job_title TEXT, description_text TEXT)");
            st.executeUpdate("CREATE TABLE IF NOT EXISTS analysis_results (" +
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, resume_id INTEGER, job_id INTEGER, ats_score REAL, " +
                    "matched_skills TEXT, missing_skills TEXT, suggestions TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, " +
                    "FOREIGN KEY (resume_id) REFERENCES resumes(id), FOREIGN KEY (job_id) REFERENCES jobs(id))");
            log.info("SQLite schema ensured.");
        } catch (SQLException e){
            log.error("Schema init error", e);
        }
    }
}
