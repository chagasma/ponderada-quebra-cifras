import random
import math
from typing import List, Tuple


class PermutationBreaker:
    def __init__(self, scorer):
        self.scorer = scorer

    def _columnar_decrypt(self, ciphertext: str, key: List[int]) -> str:
        ciphertext = ciphertext.upper().replace(' ', '').replace('\n', '')
        n_cols = len(key)
        n_rows = math.ceil(len(ciphertext) / n_cols)

        grid = [[''] * n_cols for _ in range(n_rows)]

        idx = 0
        for col_order in sorted(range(n_cols), key=lambda x: key[x]):
            for row in range(n_rows):
                if idx < len(ciphertext):
                    grid[row][col_order] = ciphertext[idx]
                    idx += 1

        plaintext = ''.join(''.join(row) for row in grid)
        return plaintext

    def _simulated_annealing(
        self,
        ciphertext: str,
        key_length: int,
        temperature: float = 20.0,
        cooling_rate: float = 0.995,
        iterations: int = 50000
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

    def break_cipher(self, ciphertext: str, key_length: int) -> Tuple[str, List[int]]:
        best_key, plaintext = self._simulated_annealing(ciphertext, key_length)
        return plaintext, best_key
