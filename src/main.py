import sys
from pathlib import Path
from utils.ngram_scorer import NgramScorer
from breakers.substitution_breaker import SubstitutionBreaker
from breakers.permutation_breaker import PermutationBreaker


class CipherBreakerTester:
    def __init__(self, ngram_file: str):
        self.scorer = NgramScorer(ngram_file)
        self.sub_breaker = SubstitutionBreaker(self.scorer)
        self.perm_breaker = PermutationBreaker(self.scorer)

    def test_substitution(self, ciphertext_path: Path) -> dict:
        with open(ciphertext_path, 'r') as f:
            ciphertext = f.read().strip()

        plaintext, mapping = self.sub_breaker.break_cipher(ciphertext)
        return {
            'file': ciphertext_path.name,
            'ciphertext': ciphertext,
            'plaintext': plaintext,
            'mapping': mapping,
            'score': self.scorer.score(plaintext)
        }

    def test_permutation(self, ciphertext_path: Path, key_length: int) -> dict:
        with open(ciphertext_path, 'r') as f:
            ciphertext = f.read().strip()

        plaintext, key = self.perm_breaker.break_cipher(ciphertext, key_length)
        return {
            'file': ciphertext_path.name,
            'ciphertext': ciphertext,
            'plaintext': plaintext,
            'key': key,
            'score': self.scorer.score(plaintext)
        }

    def test_all_substitution(self, cipher_dir: Path):
        print("="*80)
        print("SUBSTITUTION CIPHER BREAKING")
        print("="*80)

        files = sorted(cipher_dir.glob('substitution_*.txt'))
        for cipher_file in files:
            result = self.test_substitution(cipher_file)
            self._print_result(result)

    def test_all_permutation(self, cipher_dir: Path, key_length: int = 5):
        print("\n" + "="*80)
        print("PERMUTATION CIPHER BREAKING")
        print("="*80)

        files = sorted(cipher_dir.glob('permutation_*.txt'))
        for cipher_file in files:
            result = self.test_permutation(cipher_file, key_length)
            self._print_result(result)

    def _print_result(self, result: dict):
        print(f"\nFile: {result['file']}")
        print(f"Ciphertext: {result['ciphertext'][:60]}...")
        print(f"Plaintext:  {result['plaintext'][:60]}...")
        print(f"Score: {result['score']:.2f}")
        if 'mapping' in result:
            print(f"Mapping: {dict(list(result['mapping'].items())[:10])}...")
        if 'key' in result:
            print(f"Key: {result['key']}")


def main():
    base_dir = Path(__file__).parent.parent
    ngram_file = base_dir / 'data' / 'english_quadgrams.txt'
    cipher_dir = base_dir / 'data' / 'ciphertexts'

    tester = CipherBreakerTester(str(ngram_file))

    if len(sys.argv) > 1:
        cipher_type = sys.argv[1].lower()
        if cipher_type == 'sub':
            tester.test_all_substitution(cipher_dir)
        elif cipher_type == 'perm':
            key_len = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            tester.test_all_permutation(cipher_dir, key_len)
        else:
            print("Usage: python main.py [sub|perm] [key_length]")
    else:
        tester.test_all_substitution(cipher_dir)
        tester.test_all_permutation(cipher_dir)


if __name__ == '__main__':
    main()
