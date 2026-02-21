package com.sra.backend.config;

import javax.sql.DataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.sqlite.SQLiteDataSource;

@Configuration
public class DatabaseConfig {
    @Value("${sra.db.path:data/smart_resume_analyzer.db}")
    private String dbPath;

    @Bean
    public DataSource dataSource(){
        SQLiteDataSource ds = new SQLiteDataSource();
        ds.setUrl("jdbc:sqlite:" + dbPath);
        return ds;
    }
}
