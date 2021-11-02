package ru.itukh.spellchecker;

import opennlp.tools.tokenize.SimpleTokenizer;
import org.apache.commons.codec.EncoderException;
import org.languagetool.JLanguageTool;
import org.languagetool.language.AmericanEnglish;
import org.languagetool.rules.RuleMatch;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class SpellChecker {
    private final SimpleTokenizer tokenizer = SimpleTokenizer.INSTANCE;
    private final JLanguageTool langTool = new JLanguageTool(new AmericanEnglish());
    private final CandidatesRanker ranker = new CandidatesRanker();

    public void check(String text) throws IOException, EncoderException {
        String[] tokens = tokenizer.tokenize(text);
        for (String token : tokens) {
            List<RuleMatch> matches = langTool.check(token);
            List<String> replacements = new ArrayList<>();
            for (RuleMatch match : matches) {
                replacements.addAll(match.getSuggestedReplacements());
            }
            if (matches.size() == 0) {
                continue;
            }
            System.out.println("Unknown word: " + token + ". Possible corrections:");
            for (String replacement: ranker.rank(token, replacements)) {
                System.out.println("- " + replacement);
            }
        }
    }
}
