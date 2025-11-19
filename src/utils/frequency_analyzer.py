"""
Análise de frequências para quebra de cifras de substituição.
Utiliza frequências de caracteres calculadas a partir de arquivo CSV de unigramas.
"""

import string
import csv
from pathlib import Path
from collections import Counter
from typing import Dict, List, Tuple, Optional
import math


class FrequencyAnalyzer:
    """
    Analisador de frequências para cifras de substituição monoalfabéticas.
    Calcula frequências de caracteres a partir de arquivo CSV de unigramas.
    """
    
    # Valores padrão (fallback se CSV não for encontrado)
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
        Inicializa o analisador de frequências.
        
        Args:
            unigram_csv_file: Caminho para arquivo CSV com frequências de unigramas.
                            Se None, tenta carregar de data/unigram_freq.csv
        """
        self.alphabet = string.ascii_uppercase
        
        # Define caminho padrão
        if unigram_csv_file is None:
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent
            unigram_csv_file = project_root / "data" / "unigram_freq.csv"
        else:
            unigram_csv_file = Path(unigram_csv_file)
        
        # Carrega frequências de caracteres do CSV
        self.char_frequencies, self.freq_order = self._load_char_frequencies_from_csv(
            unigram_csv_file
        )
    
    def _load_char_frequencies_from_csv(
        self, 
        csv_file: Path
    ) -> Tuple[Dict[str, float], str]:
        """
        Carrega frequências de caracteres calculadas a partir de CSV de unigramas.
        
        O CSV contém palavras e suas frequências. Calculamos a frequência de cada
        letra somando as ocorrências em todas as palavras, ponderadas pela frequência
        de cada palavra.
        
        Args:
            csv_file: Caminho para arquivo CSV (formato: word,count)
            
        Returns:
            Tupla (dicionário de frequências, ordem de frequência)
        """
        if not csv_file.exists():
            print(
                f"Aviso: Arquivo CSV não encontrado: {csv_file}\n"
                f"Usando valores padrão."
            )
            return self.DEFAULT_CHAR_FREQUENCIES.copy(), self.DEFAULT_FREQ_ORDER
        
        try:
            char_counter = Counter()
            total_char_count = 0
            
            print(f"Carregando frequências de caracteres de: {csv_file}")
            print("Processando arquivo CSV (isso pode levar alguns segundos)...")
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                processed = 0
                for row in reader:
                    word = row.get('word', '').upper().strip()
                    try:
                        count = int(row.get('count', 0))
                    except (ValueError, TypeError):
                        continue
                    
                    # Conta cada letra na palavra, ponderada pela frequência da palavra
                    for char in word:
                        if char.isalpha() and char in self.alphabet:
                            char_counter[char] += count
                            total_char_count += count
                    
                    processed += 1
                    if processed % 50000 == 0:
                        print(f"  Processadas {processed} palavras...")
            
            print(f"Processadas {processed} palavras")
            print(f"Total de caracteres contados: {total_char_count:,}")
            
            # Calcula frequências percentuais
            frequencies = {}
            for char in self.alphabet:
                count = char_counter.get(char, 0)
                frequencies[char] = (count / total_char_count * 100.0) if total_char_count > 0 else 0.0
            
            # Ordena por frequência
            sorted_freq = sorted(
                frequencies.items(),
                key=lambda x: x[1],
                reverse=True
            )
            freq_order = ''.join(char for char, _ in sorted_freq)
            
            print(f"Frequencias calculadas. Ordem: {freq_order}")
            print(f"  Letra mais frequente: {freq_order[0]} ({frequencies[freq_order[0]]:.2f}%)")
            
            return frequencies, freq_order
            
        except Exception as e:
            print(
                f"Erro ao carregar CSV {csv_file}: {e}\n"
                f"Usando valores padrão."
            )
            return self.DEFAULT_CHAR_FREQUENCIES.copy(), self.DEFAULT_FREQ_ORDER
    
    def calculate_char_frequencies(self, text: str) -> Dict[str, float]:
        """
        Calcula frequências de caracteres no texto.
        
        Args:
            text: Texto para análise
            
        Returns:
            Dicionário com frequências percentuais de cada letra
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
        Calcula o Índice de Coincidência (IC) do texto.
        
        O IC mede a probabilidade de duas letras aleatórias serem iguais.
        Para inglês: ~0.0667
        Para texto aleatório: ~0.0385
        
        Args:
            text: Texto para análise
            
        Returns:
            Índice de coincidência (0.0 a 1.0)
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
        Analisa bigramas no texto.
        
        Args:
            text: Texto para análise
            
        Returns:
            Dicionário com contagem de bigramas
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
        Analisa trigramas no texto.
        
        Args:
            text: Texto para análise
            
        Returns:
            Dicionário com contagem de trigramas
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
        Calcula chi-quadrado para avaliar qualidade do mapeamento.
        
        Compara frequências observadas com frequências esperadas do inglês.
        
        Args:
            text: Texto decifrado
            mapping: Mapeamento usado
            
        Returns:
            Valor do chi-quadrado (menor é melhor)
        """
        frequencies = self.calculate_char_frequencies(text)
        chi_squared = 0.0
        
        for char in self.alphabet:
            observed = frequencies.get(char, 0.0)
            expected = self.char_frequencies.get(char, 0.0)
            
            if expected > 0:
                chi_squared += ((observed - expected) ** 2) / expected
        
        return chi_squared

