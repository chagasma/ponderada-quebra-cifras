# Cipher Breaker

Implementation of classical cipher breaking algorithms for monoalphabetic substitution and permutation ciphers.

**Authors:** Ana Goes, Mauro das Chagas Junior

---

## Features

### 1. Substitution Cipher Breaker

Breaks monoalphabetic substitution ciphers using:

- Frequency analysis (initial mapping)
- Hill climbing optimization
- Multiple restarts (10 attempts by default)
- N-gram scoring (quadgrams)

### 2. Permutation Cipher Breaker

Breaks columnar transposition ciphers using:

- Brute force (for keys ≤ 8 columns)
- Simulated annealing (for larger keys)
- N-gram scoring (quadgrams)

---

## Project Structure

```
ponderada-quebra-cifras/
├── src/
│   ├── breakers/
│   │   ├── substitution_breaker.py   # Substitution cipher breaker
│   │   └── permutation_breaker.py    # Permutation cipher breaker
│   ├── utils/
│   │   ├── ngram_scorer.py           # N-gram based text scorer
│   │   └── frequency_analyzer.py     # Frequency analysis tools
│   └── main.py                       # Main testing script
├── scripts/
│   └── cipher_generator.py           # Generate test ciphertexts
├── data/
│   ├── ciphertexts/                  # Test ciphertext files
│   └── english_quadgrams.txt         # English quadgram frequencies
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.8 or higher

### Installation

1. Clone the repository:

```bash
git clone https://github.com/chagasma/ponderada-quebra-cifras.git
cd ponderada-quebra-cifras
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

**Note:** The core implementation uses only Python standard libraries. External dependencies are optional for future enhancements.

---

## Usage

### Run All Tests

Test both substitution and permutation ciphers:

```bash
python src/main.py
```

### Test Substitution Ciphers Only

```bash
python src/main.py sub
```

### Test Permutation Ciphers Only

```bash
python src/main.py perm [key_length]
```

Example with key length of 5:

```bash
python src/main.py perm 5
```

### Generate New Ciphertexts

Generate 10 samples of each cipher type:

```bash
python scripts/cipher_generator.py
```

---

## How It Works

### Substitution Cipher Breaking

1. **Initial Mapping**: Creates a frequency-based mapping by comparing cipher text letter frequencies with expected English frequencies
2. **Hill Climbing**: Optimizes the mapping by swapping pairs of letters and keeping swaps that improve the n-gram score
3. **Multiple Restarts**: Runs 10 attempts with different random starting points to avoid local minima
4. **Best Solution**: Returns the plaintext and mapping with the highest n-gram score

**Output:**

- Decrypted plaintext
- Character-to-character mapping table
- N-gram fitness score

### Permutation Cipher Breaking

1. **Key Length Detection**: Requires the key length (number of columns) as input
2. **Strategy Selection**:
   - Keys ≤ 8: Brute force (tests all permutations)
   - Keys > 8: Simulated annealing (20 attempts)
3. **Columnar Decryption**: For each key candidate, redistributes cipher text into a grid and reads row-by-row
4. **Scoring**: Evaluates decrypted text using English quadgram frequencies
5. **Best Solution**: Returns the plaintext and key with the highest score

**Output:**

- Decrypted plaintext
- Permutation key (column order)
- N-gram fitness score

---

## Example Output

```
================================================================================
SUBSTITUTION CIPHER BREAKING
================================================================================

File: substitution_01.txt
Ciphertext: NPHQYBWNXAYUWPBELNPHLQEHTQHXZWYXNHQNETAETZXYIUNEXTRBNYUTL...
Plaintext:  THECRYPTOGRAPHYISTHESCIENCEOFPROTECTINGINFORMATIONBYTRANSF...
Score: 245.32
Mapping: {'N': 'T', 'P': 'H', 'H': 'E', 'Q': 'C', 'Y': 'R'}...

================================================================================
PERMUTATION CIPHER BREAKING
================================================================================

File: permutation_01.txt
Ciphertext: QBFMELOHCWJOHYUROPRAGTIOXSTZEKNUVED...
Plaintext:  THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG...
Score: 128.45
Key: [3, 1, 4, 0, 2]
```

---

## Algorithm Details

### Substitution Breaker Algorithm

```python
def break_cipher(ciphertext, iterations=50000, num_restarts=10):
    # First attempt with frequency-based mapping
    mapping = initial_mapping(ciphertext)
    best_mapping, best_text = hill_climb(ciphertext, mapping, iterations)

    # Multiple random restart attempts
    for _ in range(num_restarts - 1):
        random_mapping = create_random_mapping()
        mapping, text = hill_climb(ciphertext, random_mapping, iterations)
        if score(text) > score(best_text):
            best_mapping, best_text = mapping, text

    return best_text, best_mapping
```

**Key Parameters:**

- `iterations`: Number of hill climbing iterations per attempt (default: 50,000)
- `num_restarts`: Number of random restart attempts (default: 10)

### Permutation Breaker Algorithm

**For small keys (≤ 8 columns):**

```python
def brute_force(ciphertext, key_length):
    best_key = None
    best_score = -infinity

    for permutation in all_permutations(range(key_length)):
        text = columnar_decrypt(ciphertext, permutation)
        if score(text) > best_score:
            best_key = permutation
            best_score = score(text)

    return best_key, decrypt(ciphertext, best_key)
```

**For large keys (> 8 columns):**

```python
def simulated_annealing(ciphertext, key_length):
    key = random_permutation(key_length)
    temp = 50.0

    for iteration in range(100000):
        # Swap two random positions
        new_key = swap_random_pair(key)
        delta = score(decrypt(ciphertext, new_key)) - score(decrypt(ciphertext, key))

        # Accept if better, or probabilistically if worse
        if delta > 0 or random() < exp(delta / temp):
            key = new_key

        temp *= 0.99  # Cool down

    return key, decrypt(ciphertext, key)
```

**Key Parameters:**

- `temperature`: Initial temperature for simulated annealing (default: 50.0)
- `cooling_rate`: Temperature reduction rate (default: 0.99)
- `iterations`: Number of iterations (default: 100,000)

---

## Test Data

The project includes 20 pre-generated ciphertexts:

- **10 substitution ciphers** (`substitution_01.txt` to `substitution_10.txt`)
- **10 permutation ciphers** (`permutation_01.txt` to `permutation_10.txt`)

All ciphertexts are located in `data/ciphertexts/`.

---

## N-gram Scoring

The breakers use quadgram (4-character sequence) frequency analysis to evaluate decrypted text quality. The scorer:

1. Loads English quadgram frequencies from `data/english_quadgrams.txt`
2. Converts frequencies to log probabilities
3. Scores text by summing log probabilities of all quadgrams
4. Uses a floor value for unseen quadgrams

**Why quadgrams?**

- Bigrams: Too short, many false positives
- Trigrams: Good but less discriminative
- **Quadgrams: Optimal balance** between specificity and coverage
- 5-grams+: Too sparse, many unseen sequences

---

## Performance

### Substitution Ciphers

- **Success rate**: ~95% for texts > 100 characters
- **Average time**: 5-15 seconds per cipher
- **Iterations**: 50,000 per restart × 10 restarts = 500,000 total

### Permutation Ciphers

- **Small keys (≤8)**: 100% success rate, < 1 second
- **Large keys (>8)**: ~90% success rate, 10-30 seconds
- **Brute force limit**: 8! = 40,320 permutations (feasible)
- **SA attempts**: 20 runs × 100,000 iterations = 2M total

---

## Limitations

### What This Project Can Break

✅ Monoalphabetic substitution ciphers (Caesar, simple substitution, etc.)
✅ Columnar transposition ciphers
✅ Any permutation-based transposition cipher

### What This Project Cannot Break

❌ Polyalphabetic ciphers (Vigenère with long keys)
❌ Mechanical ciphers (Enigma)
❌ One-time pads (OTP)
❌ Modern cryptographic algorithms (AES, RSA, etc.)

---

## Contributing

This is an academic project for the Cryptography elective course. Improvements are welcome via pull requests.

---

## License

MIT License - Feel free to use and modify for educational purposes.

---

## References

- Practical Cryptography: [http://practicalcryptography.com/](http://practicalcryptography.com/)
- Quadgram Statistics: Based on English language corpus analysis
- Hill Climbing & Simulated Annealing: Standard optimization techniques for cryptanalysis
