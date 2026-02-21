// src/main/java/com/sra/backend/service/OpenAIClientAdapter.java
package com.sra.backend.service;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Real OpenAI client adapter using the official openai-java 4.x SDK.
 * - Reads API key from constructor or falls back to OPENAI_API_KEY env var.
 * - Uses Chat Completions with model "gpt-4o-mini".
 * - Returns the first choice text or a safe fallback if unavailable.
 */
public class OpenAIClientAdapter implements AIClientAdapter {

    private static final Logger log = LogManager.getLogger(OpenAIClientAdapter.class);
    private static final String DEFAULT_MODEL = "gpt-4o-mini";

    private final OpenAIClient client;

    /**
     * If {@code apiKey} is null/blank, the client loads OPENAI_API_KEY (and related vars)
     * from environment/system properties via OpenAIOkHttpClient.fromEnv().
     */
    public OpenAIClientAdapter(String apiKey) {
        this.client = (apiKey != null && !apiKey.isBlank())
                ? OpenAIOkHttpClient.builder().apiKey(apiKey).build()
                : OpenAIOkHttpClient.fromEnv();
    }

    @Override
    public String generateAdvice(String prompt) {
        if (prompt == null || prompt.isBlank()) {
            log.warn("generateAdvice called with empty prompt");
            return "No prompt provided.";
        }

        try {
            ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                    .addUserMessage(prompt)
                    // You can swap the model via config/env if you prefer:
                    .model(DEFAULT_MODEL)
                    .temperature(0.2)
                    // In 4.x this is maxCompletionTokens (not maxTokens)
                    .maxCompletionTokens(220)
                    .build();

            ChatCompletion completion = client
                    .chat()
                    .completions()
                    .create(params);

            String text = completion.choices().stream()
                    .findFirst()
                    .flatMap(choice -> choice.message().content())
                    .orElse("");

            if (text.isBlank()) {
                log.warn("OpenAI returned empty content. Using fallback message.");
                return "No specific suggestions available at the moment.";
            }

            return text.trim();

        } catch (Exception e) {
            log.error("OpenAI suggestion generation failed", e);
            // Safe fallback to keep your API stable even if OpenAI is down/misconfigured.
            return "Consider focusing on the missing skills with concise bullets, "
                    + "adding relevant certifications (e.g., AWS, Docker), and tailoring "
                    + "your summary to the job role to improve ATS alignment.";
        }
    }
}
