package com.sra.backend.dao;

import com.sra.backend.model.AnalysisResult;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ResultDAO {
    private static final Logger log = LogManager.getLogger(ResultDAO.class);
    private final DataSource ds;
    public ResultDAO(DataSource ds){ this.ds = ds; }

    public boolean insertResult(AnalysisResult ar){
        String sql = "INSERT INTO analysis_results(resume_id, job_id, ats_score, matched_skills, missing_skills, suggestions) VALUES(?,?,?,?,?,?)";
        try(Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)){
            ps.setLong(1, ar.getResumeId()); ps.setLong(2, ar.getJobId()); ps.setDouble(3, ar.getAtsScore());
            ps.setString(4, ar.getMatchedSkills()); ps.setString(5, ar.getMissingSkills()); ps.setString(6, ar.getSuggestions());
            ps.executeUpdate(); try(ResultSet rs = ps.getGeneratedKeys()){ if(rs.next()) ar.setId(rs.getLong(1)); }
            log.info("Inserted analysis result for resumeId={}, jobId={}", ar.getResumeId(), ar.getJobId());
            return true;
        } catch(SQLException e){ log.error("Insert result failed", e); return false; }
    }

    public AnalysisResult findById(long id){
        String sql = "SELECT id,resume_id,job_id,ats_score,matched_skills,missing_skills,suggestions,datetime(timestamp) as ts FROM analysis_results WHERE id=?";
        try(Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement(sql)){
            ps.setLong(1, id); try(ResultSet rs = ps.executeQuery()){
                if(rs.next()){
                    return new AnalysisResult(
                        rs.getLong("id"),
                        rs.getLong("resume_id"),
                        rs.getLong("job_id"),
                        rs.getDouble("ats_score"),
                        rs.getString("matched_skills"),
                        rs.getString("missing_skills"),
                        rs.getString("suggestions"),
                        rs.getString("ts")
                    );
                }
            }
        } catch(SQLException e){ log.error("Find result failed", e); }
        return null;
    }
}
