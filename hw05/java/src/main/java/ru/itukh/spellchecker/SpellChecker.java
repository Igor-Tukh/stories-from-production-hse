package ru.itukh.spellchecker;

import opennlp.tools.tokenize.SimpleTokenizer;
import org.languagetool.JLanguageTool;
import org.languagetool.language.AmericanEnglish;
import org.languagetool.rules.RuleMatch;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class SpellChecker {
    public static void check(String text) throws IOException {
        SimpleTokenizer tokenizer = SimpleTokenizer.INSTANCE;
        String[] tokens = tokenizer.tokenize(text);
        JLanguageTool langTool = new JLanguageTool(new AmericanEnglish());
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
            for (String replacement: replacements) {
                System.out.println("- " + replacement);
            }
        }
    }
}
