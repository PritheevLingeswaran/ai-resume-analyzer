package com.sra.backend.config;

import com.sra.backend.dao.DatabaseUtil;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;

@Configuration
public class SchemaInitializer {
    @Bean
    CommandLineRunner init(DataSource ds){
        return args -> DatabaseUtil.createSchemaIfNeeded(ds);
    }
}
