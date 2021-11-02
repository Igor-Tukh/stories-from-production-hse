package ru.itukh.spellchecker;

import info.debatty.java.stringsimilarity.Levenshtein;

import java.util.ArrayList;
import java.util.List;

public class CandidatesRanker {
    public static List<String> rank(String word, List<String> candidates) {
        List<Double> similarities = new ArrayList<>();
        Levenshtein distanceMeasurer = new Levenshtein();
        for (String candidate : candidates) {
            similarities.add(distanceMeasurer.distance(word, candidate));
        }
        return candidates;
    }
}
