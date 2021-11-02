import nltk
import os

from hunspell import Hunspell
from nltk.tokenize import word_tokenize

from src.candidates_ranker import CandidatesRanker

dictionaries = {
    'english': 'en_US',
}


class SpellChecker:
    def __init__(self, language, n_suggestions):
        self.language = language
        self.hunspell = Hunspell(dictionaries[language])
        self.n_suggestions = n_suggestions
        nltk.download('punkt', quiet=True)
        self.ranker = CandidatesRanker(language)

    def __call__(self, text):
        words = word_tokenize(text, self.language)
        for word in words:
            if self.hunspell.spell(word):
                continue
            print(f'Unknown word: \'{word}\'.', end=' ')
            candidates = self._collect_candidates(word)
            print('Possible corrections (from the most probable to the least probable):' if len(candidates) > 0 else
                  'No corrections found.')
            candidates = self._rank_candidates(word, candidates)
            candidates = candidates[:min(len(candidates), self.n_suggestions)]
            print(os.linesep.join(candidates))

    def _collect_candidates(self, word):
        return self.hunspell.suggest(word)

    def _rank_candidates(self, word, candidates):
        return self.ranker(word, candidates)
