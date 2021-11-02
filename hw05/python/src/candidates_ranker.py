import numpy as np
import jaro
import textdistance

from pyphonetics import RefinedSoundex
from wordfreq import word_frequency

language_macros = {
    'english': 'en',
}

eps = 1e-9


class CandidatesRanker:
    def __init__(self, language):
        self.rs = RefinedSoundex()
        self.language = language_macros[language]

    def __call__(self, word, candidates):
        if len(candidates) == 0:
            return []
        distances = []
        for candidate in candidates:
            levenshtein_phonetic_distance = self.rs.distance(word, candidate, metric='levenshtein')
            jaro_winkler_distance = 1 - jaro.jaro_winkler_metric(word, candidate)
            hamming_distance = textdistance.hamming(word, candidate)
            levenshtein_distance = textdistance.levenshtein(word, candidate)
            word_freq = 1 - word_frequency(candidate, self.language)
            distances.append([levenshtein_phonetic_distance,
                              jaro_winkler_distance,
                              hamming_distance,
                              levenshtein_distance,
                              word_freq])
        distances = np.array(distances)
        weights = ((distances - distances.min(axis=0) + eps) / (distances.max(axis=0) - distances.min(axis=0) + eps)).mean(axis=1)
        return list(np.array(candidates)[np.argsort(weights)])
