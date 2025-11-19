"""
Quebrador de cifras de substituição monoalfabéticas.
Utiliza heurísticas de frequência e hill climbing para quebrar cifras.
"""

import random
import string
from typing import Dict, Tuple, Optional
from copy import deepcopy

from ..utils.frequency_analyzer import FrequencyAnalyzer
from ..utils.ngram_scorer import NgramScorer


class SubstitutionBreaker:
    """
    Quebrador de cifras de substituição monoalfabéticas.
    
    Utiliza duas heurísticas principais:
    1. Análise de frequências de caracteres
    2. Hill climbing para otimização do mapeamento
    """
    
    def __init__(
        self, 
        ngram_file: str,
        n: int = 4,
        max_iterations: int = 10000,
        num_restarts: int = 5,
        use_soft_climbing: bool = True,
        unigram_csv_file: str = None
    ):
        """
        Inicializa o quebrador de cifras.
        
        Args:
            ngram_file: Caminho para arquivo de n-gramas
            n: Tamanho dos n-gramas (padrão: 4 para quadgrams)
            max_iterations: Número máximo de iterações do hill climbing
            num_restarts: Número de reinicializações para evitar mínimos locais
            use_soft_climbing: Se True, usa hill climbing suave (aceita soluções piores)
            unigram_csv_file: Caminho para CSV de unigramas (None = usa padrão)
        """
        self.scorer = NgramScorer(ngram_file, n)
        self.frequency_analyzer = FrequencyAnalyzer(unigram_csv_file=unigram_csv_file)
        self.letters = string.ascii_uppercase
        self.max_iterations = max_iterations
        self.num_restarts = num_restarts
        self.use_soft_climbing = use_soft_climbing
    
    def _decrypt(
        self, 
        ciphertext: str, 
        mapping: Dict[str, str]
    ) -> str:
        """
        Aplica mapeamento ao texto cifrado para descriptografar.
        
        Args:
            ciphertext: Texto cifrado
            mapping: Mapeamento de caracteres (cifrado -> claro)
            
        Returns:
            Texto descriptografado
        """
        result = []
        for c in ciphertext.upper():
            if c.isalpha():
                result.append(mapping.get(c, c))
            else:
                result.append(c)
        return ''.join(result)
    
    def _create_initial_mapping(
        self, 
        ciphertext: str,
        use_frequency: bool = True
    ) -> Dict[str, str]:
        """
        Cria mapeamento inicial usando análise de frequências.
        
        Args:
            ciphertext: Texto cifrado
            use_frequency: Se True, usa análise de frequências; caso contrário, aleatório
            
        Returns:
            Mapeamento inicial de caracteres
        """
        if use_frequency:
            # Usa análise de frequências
            mapping = self.frequency_analyzer.create_frequency_mapping(ciphertext)
        else:
            # Mapeamento aleatório
            mapping = self._random_mapping()
        
        return mapping
    
    def _random_mapping(self) -> Dict[str, str]:
        """
        Cria mapeamento aleatório.
        
        Returns:
            Mapeamento aleatório de caracteres
        """
        plain_chars = list(self.letters)
        random.shuffle(plain_chars)
        return {
            cipher: plain 
            for cipher, plain in zip(self.letters, plain_chars)
        }
    
    def _swap_mapping(
        self, 
        mapping: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Gera vizinho trocando dois valores no mapeamento.
        
        Args:
            mapping: Mapeamento atual
            
        Returns:
            Novo mapeamento com dois caracteres trocados
        """
        new_mapping = deepcopy(mapping)
        
        # Seleciona dois caracteres aleatórios para trocar
        a, b = random.sample(self.letters, 2)
        new_mapping[a], new_mapping[b] = new_mapping[b], new_mapping[a]
        
        return new_mapping
    
    def _hill_climb(
        self, 
        ciphertext: str, 
        initial_mapping: Dict[str, str],
        use_soft_climbing: bool = True,
        initial_acceptance_prob: float = 0.3,
        cooling_rate: float = 0.999
    ) -> Tuple[Dict[str, str], str, float]:
        """
        Executa algoritmo de hill climbing (suave) para otimizar o mapeamento.
        
        Hill climbing suave aceita soluções piores com probabilidade que diminui
        ao longo das iterações, permitindo escapar de mínimos locais.
        
        Args:
            ciphertext: Texto cifrado
            initial_mapping: Mapeamento inicial
            use_soft_climbing: Se True, usa hill climbing suave (aceita soluções piores)
            initial_acceptance_prob: Probabilidade inicial de aceitar solução pior (0.0-1.0)
            cooling_rate: Taxa de resfriamento da probabilidade (0.0-1.0)
            
        Returns:
            Tupla (melhor_mapeamento, melhor_texto, melhor_score)
        """
        current_mapping = deepcopy(initial_mapping)
        current_text = self._decrypt(ciphertext, current_mapping)
        current_score = self.scorer.score(current_text)
        
        best_mapping = deepcopy(current_mapping)
        best_text = current_text
        best_score = current_score
        
        # Contador de iterações sem melhoria
        no_improvement_count = 0
        max_no_improvement = self.max_iterations // 10
        
        # Probabilidade atual de aceitar solução pior
        acceptance_prob = initial_acceptance_prob if use_soft_climbing else 0.0
        
        for iteration in range(self.max_iterations):
            # Gera vizinho trocando dois caracteres
            neighbor_mapping = self._swap_mapping(current_mapping)
            neighbor_text = self._decrypt(ciphertext, neighbor_mapping)
            neighbor_score = self.scorer.score(neighbor_text)
            
            # Calcula diferença de score
            score_diff = neighbor_score - current_score
            
            # Se o vizinho é melhor, aceita sempre
            if score_diff > 0:
                current_mapping = neighbor_mapping
                current_text = neighbor_text
                current_score = neighbor_score
                no_improvement_count = 0
                
                # Atualiza melhor global
                if neighbor_score > best_score:
                    best_mapping = deepcopy(neighbor_mapping)
                    best_text = neighbor_text
                    best_score = neighbor_score
            else:
                # Vizinho é pior ou igual
                if use_soft_climbing and acceptance_prob > 0:
                    # Aceita solução pior com probabilidade (diminui ao longo do tempo)
                    if random.random() < acceptance_prob:
                        current_mapping = neighbor_mapping
                        current_text = neighbor_text
                        current_score = neighbor_score
                        no_improvement_count = 0
                        
                        # Reduz probabilidade de aceitação
                        acceptance_prob *= cooling_rate
                    else:
                        no_improvement_count += 1
                else:
                    # Hill climbing tradicional: rejeita sempre
                    no_improvement_count += 1
            
            # Se não há melhoria há muito tempo, faz um "salto"
            if no_improvement_count > max_no_improvement:
                # Faz uma troca aleatória para escapar de mínimo local
                current_mapping = self._swap_mapping(current_mapping)
                current_text = self._decrypt(ciphertext, current_mapping)
                current_score = self.scorer.score(current_text)
                no_improvement_count = 0
                # Reinicia probabilidade de aceitação
                if use_soft_climbing:
                    acceptance_prob = initial_acceptance_prob * 0.5
        
        return best_mapping, best_text, best_score
    
    def break_cipher_frequency_only(
        self, 
        ciphertext: str
    ) -> Tuple[str, Dict[str, str], float]:
        mapping = self._create_initial_mapping(ciphertext, use_frequency=True)
        plaintext = self._decrypt(ciphertext, mapping)
        
        best_mapping = mapping
        best_text = plaintext
        best_score = self._evaluate_mapping(ciphertext, mapping)
        
        cipher_freq = self.frequency_analyzer.calculate_char_frequencies(ciphertext)
        sorted_cipher = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
        
        common_bigrams = {'TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ND', 'ON', 'EN', 'AT', 'OU', 'IT', 'IS', 'OR', 'TI', 'AS', 'TO', 'HA', 'ET'}
        
        for iteration in range(100):
            test_mapping = best_mapping.copy()
            
            if len(sorted_cipher) >= 2:
                import random
                idx1, idx2 = random.sample(range(min(15, len(sorted_cipher))), 2)
                c1, c2 = sorted_cipher[idx1][0], sorted_cipher[idx2][0]
                
                if c1 in test_mapping and c2 in test_mapping:
                    test_mapping[c1], test_mapping[c2] = test_mapping[c2], test_mapping[c1]
                    
                    test_text = self._decrypt(ciphertext, test_mapping)
                    test_score = self._evaluate_mapping(ciphertext, test_mapping)
                    
                    if test_score < best_score:
                        best_score = test_score
                        best_mapping = test_mapping
                        best_text = test_text
        
        chi = self.frequency_analyzer.calculate_chi_squared(best_text, best_mapping)
        return best_text, best_mapping, chi
    
    def _evaluate_mapping(self, ciphertext: str, mapping: Dict[str, str]) -> float:
        plaintext = self._decrypt(ciphertext, mapping)
        chi = self.frequency_analyzer.calculate_chi_squared(plaintext, mapping)
        
        letters_only = ''.join(c for c in plaintext.upper() if c.isalpha())
        bigram_score = 0
        if len(letters_only) >= 2:
            common_bigrams = {'TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ND', 'ON', 'EN', 'AT', 'OU', 'IT', 'IS', 'OR', 'TI', 'AS', 'TO', 'HA', 'ET'}
            for i in range(len(letters_only) - 1):
                bigram = letters_only[i:i+2]
                if bigram in common_bigrams:
                    bigram_score += 1
        
        return chi - bigram_score * 2
    
    def break_cipher(
        self, 
        ciphertext: str,
        use_frequency_only: bool = False,
        use_frequency_initial: bool = True
    ) -> Tuple[str, Dict[str, str], float]:
        """
        Quebra a cifra usando frequências e hill climbing.
        
        Args:
            ciphertext: Texto cifrado
            use_frequency_only: Se True, usa APENAS frequência (sem hill climbing)
            use_frequency_initial: Se True, usa frequências para mapeamento inicial
            
        Returns:
            Tupla (texto_decifrado, mapeamento, score)
        """
        # Modo apenas frequência
        if use_frequency_only:
            return self.break_cipher_frequency_only(ciphertext)
        
        # Modo com hill climbing
        best_mapping = None
        best_text = None
        best_score = float('-inf')
        
        # Primeira tentativa: usa frequências
        if use_frequency_initial:
            initial_mapping = self._create_initial_mapping(
                ciphertext, 
                use_frequency=True
            )
            mapping, text, score = self._hill_climb(
                ciphertext, 
                initial_mapping,
                use_soft_climbing=self.use_soft_climbing
            )
            
            if score > best_score:
                best_mapping = mapping
                best_text = text
                best_score = score
        
        # Tentativas adicionais com mapeamentos aleatórios
        for _ in range(self.num_restarts - (1 if use_frequency_initial else 0)):
            initial_mapping = self._create_initial_mapping(
                ciphertext,
                use_frequency=False
            )
            mapping, text, score = self._hill_climb(
                ciphertext, 
                initial_mapping,
                use_soft_climbing=self.use_soft_climbing
            )
            
            if score > best_score:
                best_mapping = mapping
                best_text = text
                best_score = score
        
        return best_text, best_mapping, best_score
    
    def get_mapping_table(
        self, 
        mapping: Dict[str, str]
    ) -> str:
        """
        Formata mapeamento como tabela legível.
        
        Args:
            mapping: Mapeamento de caracteres
            
        Returns:
            String formatada com tabela de correspondência
        """
        lines = []
        lines.append("Mapeamento (Cifrado -> Claro):")
        lines.append("-" * 40)
        
        # Ordena por caractere cifrado
        sorted_items = sorted(mapping.items())
        
        for cipher, plain in sorted_items:
            lines.append(f"  {cipher} -> {plain}")
        
        return "\n".join(lines)
