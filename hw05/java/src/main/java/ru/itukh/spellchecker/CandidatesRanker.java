package ru.itukh.spellchecker;

import info.debatty.java.stringsimilarity.Levenshtein;
import org.apache.commons.codec.EncoderException;
import org.apache.commons.codec.language.Soundex;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class CandidatesRanker {
    private final Levenshtein distanceMeasurer = new Levenshtein();
    private final Soundex soundex = new Soundex();
    private static final double eps = 1e-9;

    static class Candidate implements Comparable<Candidate> {
        double rate;
        int index;

        public Candidate(double rate, int index) {
            this.rate = rate;
            this.index = index;
        }

        @Override
        public int compareTo(@NotNull CandidatesRanker.Candidate candidate) {
            if (this.rate + eps < candidate.rate || (Math.abs(candidate.rate - this.rate) < eps && this.index < candidate.index)) {
                return -1;
            } else {
                return 1;
            }
        }
    }

    public List<String> rank(String word, List<String> candidates) throws EncoderException {
        List<Double> similarities = new ArrayList<>();
        List<Integer> phoneticSimilarities = new ArrayList<>();
        for (String candidate : candidates) {
            similarities.add(distanceMeasurer.distance(word, candidate));
            phoneticSimilarities.add(4 - soundex.difference(word, candidate));
        }
        List<Candidate> ratedCandidates = new ArrayList<>();
        for (int i = 0; i < candidates.size(); ++i) {
            double currentRate = 0;
            currentRate += (similarities.get(i) - Collections.max(similarities) + eps) / (Collections.max(similarities) - Collections.min(similarities) + eps);
            currentRate += (phoneticSimilarities.get(i) - Collections.max(phoneticSimilarities) + eps) / (Collections.max(phoneticSimilarities) - Collections.min(phoneticSimilarities) + eps);
            ratedCandidates.add(new Candidate(currentRate, i));
        }
        Collections.sort(ratedCandidates);
        List<String> sortedCandidates = new ArrayList<>();
        for (Candidate c : ratedCandidates) {
            sortedCandidates.add(candidates.get(c.index));
        }
        return sortedCandidates;
    }
}
