"""
Frequency analysis for breaking substitution ciphers.
Uses character frequencies calculated from unigram CSV file.
"""

import string
import csv
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple, Optional
import math


class FrequencyAnalyzer:
    """
    Frequency analyzer for monoalphabetic substitution ciphers.
    Calculates character frequencies from unigram CSV file.
    """

    # Default values (fallback if CSV is not found)
    DEFAULT_CHAR_FREQUENCIES = {
        'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
        'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
        'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
        'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
        'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
    }
    
    DEFAULT_FREQ_ORDER = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
    
    def __init__(self, unigram_csv_file: Optional[str] = None):
        """
        Initialize the frequency analyzer.

        Args:
            unigram_csv_file: Path to CSV file with unigram frequencies.
                            If None, tries to load from data/unigram_freq.csv
        """
        self.alphabet = string.ascii_uppercase

        # Set default path
        if unigram_csv_file is None:
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent
            unigram_csv_file = project_root / "data" / "unigram_freq.csv"
        else:
            unigram_csv_file = Path(unigram_csv_file)

        # Load character frequencies from CSV
        self.char_frequencies, self.freq_order = self._load_char_frequencies_from_csv(
            unigram_csv_file
        )
    
    def _load_char_frequencies_from_csv(
        self,
        csv_file: Path
    ) -> Tuple[Dict[str, float], str]:
        """
        Load character frequencies calculated from unigram CSV.

        The CSV contains words and their frequencies. We calculate the frequency of each
        letter by summing occurrences across all words, weighted by word frequency.

        Args:
            csv_file: Path to CSV file (format: word,count)

        Returns:
            Tuple of (frequency dictionary, frequency order string)
        """
        if not csv_file.exists():
            print(
                f"Warning: CSV file not found: {csv_file}\n"
                f"Using default values."
            )
            return self.DEFAULT_CHAR_FREQUENCIES.copy(), self.DEFAULT_FREQ_ORDER
        
        try:
            char_counter = Counter()
            total_char_count = 0

            print(f"Loading character frequencies from: {csv_file}")
            print("Processing CSV file (this may take a few seconds)...")
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                processed = 0
                for row in reader:
                    word = row.get('word', '').upper().strip()
                    try:
                        count = int(row.get('count', 0))
                    except (ValueError, TypeError):
                        continue

                    # Count each letter in the word, weighted by word frequency
                    for char in word:
                        if char.isalpha() and char in self.alphabet:
                            char_counter[char] += count
                            total_char_count += count
                    
                    processed += 1
                    if processed % 50000 == 0:
                        print(f"  Processed {processed} words...")

            print(f"Processed {processed} words")
            print(f"Total characters counted: {total_char_count:,}")

            # Calculate percentage frequencies
            frequencies = {}
            for char in self.alphabet:
                count = char_counter.get(char, 0)
                frequencies[char] = (count / total_char_count * 100.0) if total_char_count > 0 else 0.0

            # Sort by frequency
            sorted_freq = sorted(
                frequencies.items(),
                key=lambda x: x[1],
                reverse=True
            )
            freq_order = ''.join(char for char, _ in sorted_freq)

            print(f"Frequencies calculated. Order: {freq_order}")
            print(f"  Most frequent letter: {freq_order[0]} ({frequencies[freq_order[0]]:.2f}%)")
            
            return frequencies, freq_order
            
        except Exception as e:
            print(
                f"Error loading CSV {csv_file}: {e}\n"
                f"Using default values."
            )
            return self.DEFAULT_CHAR_FREQUENCIES.copy(), self.DEFAULT_FREQ_ORDER
    
    def calculate_char_frequencies(self, text: str) -> Dict[str, float]:
        """
        Calculate character frequencies in the text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with percentage frequencies of each letter
        """
        text_upper = text.upper()
        letters_only = [c for c in text_upper if c.isalpha()]
        
        if not letters_only:
            return {}
        
        counter = Counter(letters_only)
        total = len(letters_only)
        
        frequencies = {}
        for char in self.alphabet:
            count = counter.get(char, 0)
            frequencies[char] = (count / total) * 100.0
        
        return frequencies
    
    def calculate_index_of_coincidence(self, text: str) -> float:
        """
        Calculate the Index of Coincidence (IC) of the text.

        IC measures the probability that two random letters are the same.
        For English: ~0.0667
        For random text: ~0.0385

        Args:
            text: Text to analyze

        Returns:
            Index of coincidence (0.0 to 1.0)
        """
        text_upper = text.upper()
        letters_only = [c for c in text_upper if c.isalpha()]
        
        if len(letters_only) < 2:
            return 0.0
        
        counter = Counter(letters_only)
        n = len(letters_only)
        
        ic = 0.0
        for count in counter.values():
            ic += count * (count - 1)
        
        ic = ic / (n * (n - 1))
        return ic
    
    def create_frequency_mapping(
        self, 
        ciphertext: str
    ) -> Dict[str, str]:
        cipher_freq = self.calculate_char_frequencies(ciphertext)
        
        if not cipher_freq:
            return {}
        
        sorted_cipher = sorted(
            cipher_freq.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        sorted_expected = sorted(
            self.char_frequencies.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        mapping = {}
        used_plain = set()
        
        for i, (cipher_char, cipher_freq_val) in enumerate(sorted_cipher):
            if cipher_char in mapping:
                continue
            
            best_match = None
            best_score = float('inf')
            
            for j, (plain_char, expected_freq_val) in enumerate(sorted_expected):
                if plain_char in used_plain:
                    continue
                
                freq_diff = abs(cipher_freq_val - expected_freq_val)
                rank_penalty = abs(i - j) * 0.5
                
                score = freq_diff + rank_penalty
                
                if score < best_score:
                    best_score = score
                    best_match = plain_char
            
            if best_match is not None:
                mapping[cipher_char] = best_match
                used_plain.add(best_match)
        
        unused_cipher = [c for c in self.alphabet if c not in mapping]
        unused_plain = [c for c in self.alphabet if c not in used_plain]
        
        for i, cipher_char in enumerate(unused_cipher):
            if i < len(unused_plain):
                mapping[cipher_char] = unused_plain[i]
            else:
                mapping[cipher_char] = cipher_char
        
        return mapping
    
    def analyze_bigrams(self, text: str) -> Dict[str, int]:
        """
        Analyze bigrams in the text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with bigram counts
        """
        text_upper = text.upper()
        letters_only = ''.join(c for c in text_upper if c.isalpha())
        
        bigrams = {}
        for i in range(len(letters_only) - 1):
            bigram = letters_only[i:i+2]
            bigrams[bigram] = bigrams.get(bigram, 0) + 1
        
        return bigrams
    
    def analyze_trigrams(self, text: str) -> Dict[str, int]:
        """
        Analyze trigrams in the text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with trigram counts
        """
        text_upper = text.upper()
        letters_only = ''.join(c for c in text_upper if c.isalpha())
        
        trigrams = {}
        for i in range(len(letters_only) - 2):
            trigram = letters_only[i:i+3]
            trigrams[trigram] = trigrams.get(trigram, 0) + 1
        
        return trigrams
    
    def calculate_chi_squared(
        self,
        text: str,
        mapping: Dict[str, str]
    ) -> float:
        """
        Calculate chi-squared to evaluate mapping quality.

        Compares observed frequencies with expected English frequencies.

        Args:
            text: Decrypted text
            mapping: Mapping used

        Returns:
            Chi-squared value (lower is better)
        """
        frequencies = self.calculate_char_frequencies(text)
        chi_squared = 0.0
        
        for char in self.alphabet:
            observed = frequencies.get(char, 0.0)
            expected = self.char_frequencies.get(char, 0.0)
            
            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected
        
        return chi_squared

