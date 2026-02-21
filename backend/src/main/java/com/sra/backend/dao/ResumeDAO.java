package com.sra.backend.dao;

import com.sra.backend.model.Resume;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ResumeDAO {
    private static final Logger log = LogManager.getLogger(ResumeDAO.class);
    private final DataSource ds;
    public ResumeDAO(DataSource ds){ this.ds = ds; }

    public boolean insertResume(Resume r){
        String sql = "INSERT INTO resumes(file_name, file_path, extracted_text) VALUES(?,?,?)";
        try(Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)){
            ps.setString(1, r.getFileName()); ps.setString(2, r.getFilePath()); ps.setString(3, r.getExtractedText());
            ps.executeUpdate();
            try(ResultSet rs = ps.getGeneratedKeys()){ if(rs.next()) r.setId(rs.getLong(1)); }
            log.info("Inserted resume: {}", r.getFileName());
            return true;
        } catch(SQLException e){ log.error("Insert resume failed", e); return false; }
    }

    public Resume fetchResumeById(long id){
        String sql = "SELECT id,file_name,file_path,extracted_text FROM resumes WHERE id=?";
        try(Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement(sql)){
            ps.setLong(1, id);
            try(ResultSet rs = ps.executeQuery()){
                if(rs.next()) return new Resume(rs.getLong(1), rs.getString(2), rs.getString(3), rs.getString(4));
            }
        } catch(SQLException e){ log.error("Fetch resume failed", e); }
        return null;
    }
}
