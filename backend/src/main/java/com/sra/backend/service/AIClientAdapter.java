package com.sra.backend.service;

/** Adapter interface to allow mocking OpenAI in tests. */
public interface AIClientAdapter {
    String generateAdvice(String prompt);
}
