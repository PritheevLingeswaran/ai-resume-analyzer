package com.sra.backend.util;

import org.springframework.web.multipart.MultipartFile;

/** Validates file type and size (<= 5MB). */
public class FileValidator {
    public static final long MAX_SIZE_BYTES = 5L * 1024 * 1024;
    public static boolean validate(MultipartFile file){
        if(file == null || file.isEmpty()) return false;
        if(file.getSize() > MAX_SIZE_BYTES) return false;
        String name = file.getOriginalFilename() == null ? "" : file.getOriginalFilename().toLowerCase();
        if(!(name.endsWith(".pdf") || name.endsWith(".docx"))) return false;
        String ct = file.getContentType();
        if(ct == null || ct.isBlank()) return true;
        return ct.equals("application/pdf") ||
               ct.equals("application/vnd.openxmlformats-officedocument.wordprocessingml.document");
    }
}
