package com.sra.backend.dao;

import com.sra.backend.model.Job;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class JobDAO {
    private static final Logger log = LogManager.getLogger(JobDAO.class);
    private final DataSource ds;
    public JobDAO(DataSource ds){ this.ds = ds; }

    public boolean insertJob(Job j){
        String sql = "INSERT INTO jobs(job_title, description_text) VALUES(?,?)";
        try(Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)){
            ps.setString(1, j.getJobTitle()); ps.setString(2, j.getDescriptionText()); ps.executeUpdate();
            try(ResultSet rs = ps.getGeneratedKeys()){ if(rs.next()) j.setId(rs.getLong(1)); }
            log.info("Inserted job: {}", j.getJobTitle()); return true;
        } catch(SQLException e){ log.error("Insert job failed", e); return false; }
    }

    public List<Job> fetchAllJobs(){
        String sql = "SELECT id,job_title,description_text FROM jobs ORDER BY id DESC";
        List<Job> out = new ArrayList<>();
        try(Connection c = ds.getConnection(); PreparedStatement ps = c.prepareStatement(sql); ResultSet rs = ps.executeQuery()){
            while(rs.next()) out.add(new Job(rs.getLong(1), rs.getString(2), rs.getString(3)));
            log.info("Fetched {} jobs", out.size());
        } catch(SQLException e){ log.error("Fetch jobs failed", e); }
        return out;
    }
}
