package com.sra.backend.controller;

import org.springframework.web.bind.annotation.*;
import java.util.List;

@CrossOrigin(origins="*")
@RestController @RequestMapping("/api")
public class JobsController {
    @GetMapping("/jobs")
    public List<String> getRoles(){
        return java.util.Arrays.asList(
            "Software Engineer","Data Analyst","AI/ML Engineer","Web Developer","Backend Developer",
            "Frontend Developer","Full Stack Developer","Mobile App Developer","DevOps Engineer","Product Manager"
        );
    }
}
