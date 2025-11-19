import math
from typing import Dict


class NgramScorer:
    def __init__(self, ngramfile: str, n: int = 4):
        self.n = n
        self.ngrams: Dict[str, float] = {}
        self.floor = None
        self._load_ngrams(ngramfile)

    def _load_ngrams(self, filename: str):
        total = 0
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    ngram, count = parts[0], int(parts[1])
                    self.ngrams[ngram] = count
                    total += count

        for ngram in self.ngrams:
            self.ngrams[ngram] = math.log10(self.ngrams[ngram] / total)

        self.floor = math.log10(0.01 / total)

    def score(self, text: str) -> float:
        text = text.upper().replace(' ', '').replace('\n', '')
        score = 0.0

        for i in range(len(text) - self.n + 1):
            ngram = text[i:i + self.n]
            if ngram in self.ngrams:
                score += self.ngrams[ngram]
            else:
                score += self.floor

        return score
