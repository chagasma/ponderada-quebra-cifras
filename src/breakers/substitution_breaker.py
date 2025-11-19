import random
import string
from collections import Counter
from typing import Dict, Tuple


class SubstitutionBreaker:
    def __init__(self, scorer):
        self.scorer = scorer
        self.letters = string.ascii_uppercase

    def _initial_mapping(self, ciphertext: str) -> Dict[str, str]:
        cipher_freq = Counter(c for c in ciphertext.upper() if c.isalpha())
        english_freq = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

        sorted_cipher = [char for char, _ in cipher_freq.most_common()]
        mapping = {}

        for i, cipher_char in enumerate(sorted_cipher):
            if i < len(english_freq):
                mapping[cipher_char] = english_freq[i]
            else:
                mapping[cipher_char] = random.choice(self.letters)

        for letter in self.letters:
            if letter not in mapping:
                available = set(self.letters) - set(mapping.values())
                if available:
                    mapping[letter] = random.choice(list(available))
                else:
                    mapping[letter] = letter

        return mapping

    def _decrypt(self, ciphertext: str, mapping: Dict[str, str]) -> str:
        result = []
        for c in ciphertext.upper():
            if c.isalpha():
                result.append(mapping.get(c, c))
            else:
                result.append(c)
        return "".join(result)

    def _hill_climb(
        self, ciphertext: str, mapping: Dict[str, str], iterations: int = 10000
    ) -> Tuple[Dict[str, str], str]:
        best_mapping = mapping.copy()
        best_text = self._decrypt(ciphertext, best_mapping)
        best_score = self.scorer.score(best_text)

        for _ in range(iterations):
            a, b = random.sample(self.letters, 2)

            mapping[a], mapping[b] = mapping[b], mapping[a]

            text = self._decrypt(ciphertext, mapping)
            score = self.scorer.score(text)

            if score > best_score:
                best_score = score
                best_mapping = mapping.copy()
                best_text = text
            else:
                mapping[a], mapping[b] = mapping[b], mapping[a]

        return best_mapping, best_text

    def break_cipher(
        self, ciphertext: str, iterations: int = 50000, num_restarts: int = 10
    ) -> Tuple[str, Dict[str, str]]:
        overall_best_mapping = None
        overall_best_text = None
        overall_best_score = float("-inf")

        mapping = self._initial_mapping(ciphertext)
        best_mapping, plaintext = self._hill_climb(ciphertext, mapping, iterations)
        score = self.scorer.score(plaintext)

        if score > overall_best_score:
            overall_best_score = score
            overall_best_mapping = best_mapping
            overall_best_text = plaintext

        for _ in range(num_restarts - 1):
            plain_chars = list(self.letters)
            random.shuffle(plain_chars)
            mapping = {c: p for c, p in zip(self.letters, plain_chars)}

            best_mapping, plaintext = self._hill_climb(ciphertext, mapping, iterations)
            score = self.scorer.score(plaintext)

            if score > overall_best_score:
                overall_best_score = score
                overall_best_mapping = best_mapping
                overall_best_text = plaintext

        return overall_best_text, overall_best_mapping
