package com.sra.backend.service;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.tokenize.SimpleTokenizer;

import java.io.InputStream;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 * NLP: lowercase + punctuation strip, tokenize (OpenNLP), POS tag if model available,
 * and extract skill-like tokens. Heuristic path now includes a small TECH_WHITELIST
 * so common tech terms (java, aws, docker, etc.) are reliably kept.
 */
@Service
public class NLPService {
    private static final Logger log = LogManager.getLogger(NLPService.class);

    private POSTaggerME posTagger;

    /** Very small stop word list to remove common function words. */
    private static final Set<String> STOP = new HashSet<>(Arrays.asList(
            "the","a","an","and","or","of","to","in","on","for","with","by","at","as",
            "is","are","be","am","was","were","this","that","these","those","from",
            "your","you","we","our","their","they","it","its","i","me","my"
    ));

    /**
     * Keep tokens that look like technologies/skills: start with a letter, then
     * letters/digits or common tech symbols (+ . # -). 2–40 chars total.
     * (Note: backslashes are doubled for Java string literals.)
     */
    private static final Pattern KEEP = Pattern.compile("^[a-z][a-z0-9+.#\\-]{1,39}$");

    /**
     * Whitelist ensures common tech tokens are always kept in the heuristic path,
     * even if the regex would be too strict for some edge cases.
     */
    private static final Set<String> TECH_WHITELIST = new HashSet<>(Arrays.asList(
            "java","python","aws","docker","spring","kafka","kubernetes","k8s",
            "sql","rest","api","apis","git","linux","react","node","nodejs",
            "mongodb","mysql","postgres","html","css","javascript","typescript",
            "terraform","gcp","azure","jenkins","gradle","maven","openapi",
            "redis","rabbitmq","spark","hadoop","java", "python", "machine learning",
            "deep learning", "tensorflow", "pytorch", "numpy", "pandas", "data analysis", "sql", "cloud",
            "aws", "docker", "kubernetes", "git", "api", "nlp", "openai"
    ));

    public NLPService() {
        try {
            InputStream model = getClass().getResourceAsStream("/models/en-pos-maxent.bin");
            if (model != null) {
                posTagger = new POSTaggerME(new POSModel(model));
                log.info("OpenNLP POS model loaded.");
            } else {
                log.warn("POS model not found; using heuristics.");
            }
        } catch (Exception e) {
            log.warn("POS model load failed; heuristics in use.", e);
        }
    }

    /** Normalize to lowercase, keep letters/digits and a few tech symbols, collapse whitespace. */
    public String preprocess(String text) {
        if (text == null) return "";
        // Keep letters/digits/+, ., #, -, and whitespace; replace everything else with spaces
        String clean = text.toLowerCase().replaceAll("[^a-z0-9+.#\\-\\s]", " ");
        // Collapse multiple spaces to single space
        return clean.replaceAll("\\s+", " ").trim();
    }

    /** Tokenize using OpenNLP SimpleTokenizer after preprocess. */
    public String[] tokenize(String text) {
        return SimpleTokenizer.INSTANCE.tokenize(preprocess(text));
    }

    /**
     * Extract keywords:
     * - If POS model available: keep nouns/adjectives + tokens matching KEEP + TECH_WHITELIST.
     * - Else (heuristics): keep tokens not in STOP and (KEEP || TECH_WHITELIST).
     */
    public List<String> extractKeywords(String text) {
        String[] toks = tokenize(text);
        if (toks.length == 0) return Collections.emptyList();

        if (posTagger == null) {
            // Heuristic path: STOP filter + (regex KEEP or whitelisted)
            List<String> out = Arrays.stream(toks)
                    .map(String::trim)
                    .filter(t -> !t.isEmpty())
                    .filter(t -> !STOP.contains(t))
                    .filter(t -> KEEP.matcher(t).matches() || TECH_WHITELIST.contains(t))
                    .distinct()
                    .collect(Collectors.toList());
            log.info("Heuristic keywords: {}", out.size());
            return out;
        }

        // POS path: allow nouns/adjectives, anything matching KEEP, and always allow whitelisted
        String[] tags = posTagger.tag(toks);
        List<String> out = new ArrayList<>();
        for (int i = 0; i < toks.length; i++) {
            String t = toks[i].trim();
            if (t.isEmpty() || STOP.contains(t)) continue;

            String tag = tags[i];
            boolean posOk = tag.startsWith("NN") || tag.equals("JJ");
            if (posOk || KEEP.matcher(t).matches() || TECH_WHITELIST.contains(t)) {
                out.add(t);
            }
        }
        List<String> dedup = out.stream().distinct().collect(Collectors.toList());
        log.info("POS keywords: {}", dedup.size());
        return dedup;
    }
}
