import random
import math
import itertools
from typing import List, Tuple


class PermutationBreaker:
    def __init__(self, scorer):
        self.scorer = scorer

    def _columnar_decrypt(self, ciphertext: str, key: List[int]) -> str:
        ciphertext = ciphertext.upper().replace(' ', '').replace('\n', '')
        n_cols = len(key)
        n_rows = math.ceil(len(ciphertext) / n_cols)

        sorted_positions = sorted(range(n_cols), key=lambda x: key[x])

        col_lengths = [n_rows] * n_cols
        remainder = len(ciphertext) % n_cols
        if remainder != 0:
            for col in range(remainder, n_cols):
                col_lengths[col] = n_rows - 1

        grid = [[''] * n_cols for _ in range(n_rows)]

        idx = 0
        for col_pos in sorted_positions:
            for row in range(col_lengths[col_pos]):
                grid[row][col_pos] = ciphertext[idx]
                idx += 1

        plaintext = ''.join(''.join(row) for row in grid)
        return plaintext.replace('', '')

    def _simulated_annealing(
        self,
        ciphertext: str,
        key_length: int,
        temperature: float = 50.0,
        cooling_rate: float = 0.99,
        iterations: int = 100000
    ) -> Tuple[List[int], str]:
        key = list(range(key_length))
        random.shuffle(key)

        best_key = key.copy()
        best_text = self._columnar_decrypt(ciphertext, best_key)
        best_score = self.scorer.score(best_text)

        current_key = key.copy()
        current_score = best_score
        temp = temperature

        for _ in range(iterations):
            i, j = random.sample(range(key_length), 2)
            current_key[i], current_key[j] = current_key[j], current_key[i]

            text = self._columnar_decrypt(ciphertext, current_key)
            score = self.scorer.score(text)

            delta = score - current_score

            if delta > 0 or random.random() < math.exp(delta / temp):
                current_score = score
                if score > best_score:
                    best_score = score
                    best_key = current_key.copy()
                    best_text = text
            else:
                current_key[i], current_key[j] = current_key[j], current_key[i]

            temp *= cooling_rate

        return best_key, best_text

    def _brute_force(self, ciphertext: str, key_length: int) -> Tuple[List[int], str]:
        best_key = None
        best_text = None
        best_score = float('-inf')

        for perm in itertools.permutations(range(key_length)):
            key = list(perm)
            text = self._columnar_decrypt(ciphertext, key)
            score = self.scorer.score(text)

            if score > best_score:
                best_score = score
                best_key = key
                best_text = text

        return best_key, best_text

    def break_cipher(self, ciphertext: str, key_length: int) -> Tuple[str, List[int]]:
        if key_length <= 8:
            key, text = self._brute_force(ciphertext, key_length)
            return text, key

        best_overall_key = None
        best_overall_text = None
        best_overall_score = float('-inf')

        for _ in range(20):
            key, text = self._simulated_annealing(ciphertext, key_length)
            score = self.scorer.score(text)

            if score > best_overall_score:
                best_overall_score = score
                best_overall_key = key
                best_overall_text = text

        return best_overall_text, best_overall_key
