# ponderada-quebra-cifras
Ponderada de quebra de cifras da optativa de criptografia. Grupo: Ana Goes, Mauro das Chagas Junior

## Algoritmo de Quebra de Cifra de Permutação (Columnar Transposition)

### Visão Geral

O algoritmo de quebra de cifra de permutação implementado neste projeto quebra cifras de transposição por colunas (columnar transposition cipher). Este tipo de cifra reorganiza o texto original em uma grade de colunas, que são então lidas em uma ordem específica determinada por uma chave numérica.

### Como é Realizada a Quebra

A quebra da cifra segue os seguintes passos:

1. **Análise do Comprimento da Chave**: O algoritmo recebe o comprimento da chave (número de colunas) como parâmetro.

2. **Escolha da Estratégia**:
   - **Chaves pequenas (≤ 8)**: Usa força bruta, testando todas as permutações possíveis da chave.
   - **Chaves grandes (> 8)**: Usa Simulated Annealing (recozimento simulado), uma meta-heurística que explora o espaço de soluções de forma inteligente.

3. **Descriptografia com Tentativa de Chave**: Para cada chave testada:
   - O texto cifrado é reorganizado em uma grade de colunas
   - As colunas são lidas na ordem especificada pela chave
   - O texto resultante é avaliado usando um scorer baseado em n-gramas

4. **Avaliação da Qualidade**: O scorer analisa o texto decifrado calculando a probabilidade de n-gramas (sequências de n caracteres) baseado em frequências do idioma inglês. Quanto maior o score, mais provável que o texto esteja correto.

5. **Seleção da Melhor Solução**: A chave que produz o texto com maior score é retornada como resultado.

### Lógica do Código

#### 1. Função `_columnar_decrypt(ciphertext, key)`

Esta função descriptografa o texto cifrado usando uma chave específica:

```python
def _columnar_decrypt(self, ciphertext: str, key: List[int]) -> str:
```

**Passos:**
- Remove espaços e quebras de linha do texto cifrado
- Calcula o número de linhas necessárias: `n_rows = ceil(len(ciphertext) / n_cols)`
- Ordena as posições das colunas de acordo com a chave (colunas menores primeiro)
- Distribui o texto cifrado nas colunas da grade, respeitando que algumas colunas podem ter uma linha a menos se o texto não preencher completamente a grade
- Lê o texto linha por linha da grade para reconstruir o texto original

**Exemplo visual:**
```
Chave: [2, 0, 1] (3 colunas)
Texto cifrado: "HLOELWRD" (8 caracteres)

Grade após distribuição:
Coluna 0: H, E, L, D
Coluna 1: L, W, R
Coluna 2: O, E

Lendo linha por linha: "HELLO WORLD"
```

#### 2. Função `_brute_force(ciphertext, key_length)`

Testa todas as permutações possíveis da chave:

```python
def _brute_force(self, ciphertext: str, key_length: int) -> Tuple[List[int], str]:
```

**Passos:**
- Gera todas as permutações possíveis de `[0, 1, 2, ..., key_length-1]`
- Para cada permutação, descriptografa o texto e calcula o score
- Retorna a chave e o texto com maior score

**Complexidade:** O(n!) onde n é o comprimento da chave. Por isso só é usado para chaves pequenas.

#### 3. Função `_simulated_annealing(ciphertext, key_length, ...)`

Usa recozimento simulado para encontrar uma boa solução sem testar todas as possibilidades:

```python
def _simulated_annealing(self, ciphertext: str, key_length: int, ...) -> Tuple[List[int], str]:
```

**Parâmetros:**
- `temperature`: Temperatura inicial (padrão: 50.0)
- `cooling_rate`: Taxa de resfriamento (padrão: 0.99)
- `iterations`: Número de iterações (padrão: 100000)

**Algoritmo:**
1. Inicializa uma chave aleatória
2. Para cada iteração:
   - Troca aleatoriamente dois elementos da chave
   - Descriptografa e avalia o novo texto
   - Se o score melhorou OU se um valor aleatório for menor que `exp(delta/temp)`, aceita a mudança
   - Reduz a temperatura multiplicando por `cooling_rate`
3. Retorna a melhor chave encontrada

**Por que funciona:** A probabilidade de aceitar soluções piores diminui com a temperatura, permitindo escapar de mínimos locais no início e convergir para uma boa solução no final.

#### 4. Função `break_cipher(ciphertext, key_length)`

Função principal que orquestra a quebra:

```python
def break_cipher(self, ciphertext: str, key_length: int) -> Tuple[str, List[int]]:
```

**Estratégia:**
- Se `key_length <= 8`: usa força bruta (garante solução ótima)
- Se `key_length > 8`: executa Simulated Annealing 20 vezes e retorna o melhor resultado (maior probabilidade de encontrar a solução correta)

### Exemplo Simples

Vamos quebrar a cifra passo a passo com um exemplo:

**Texto original:** `"HELLO WORLD"`  
**Chave usada na cifragem:** `[2, 0, 1]` (3 colunas)

#### Passo 1: Cifragem (como o texto foi cifrado originalmente)

```
1. Organiza em grade (3 colunas):
   Col 0: H E L D
   Col 1: L W R
   Col 2: O E

2. Lê na ordem da chave [2, 0, 1]:
   - Coluna 2: O E
   - Coluna 0: H E L D
   - Coluna 1: L W R
   
3. Texto cifrado: "OEHELDLWR"
```

#### Passo 2: Quebra (nosso algoritmo)

**Entrada:**
- Texto cifrado: `"OEHELDLWR"`
- Comprimento da chave: `3`

**Processo:**

1. **Tentativa com chave [0, 1, 2]:**
   ```
   Grade:
   Col 0: O E H
   Col 1: E L D
   Col 2: L W R
   
   Texto: "OEHELDLWR" → Score: -15.2 (baixo, não parece português/inglês)
   ```

2. **Tentativa com chave [1, 0, 2]:**
   ```
   Grade:
   Col 0: E L D
   Col 1: O E H
   Col 2: L W R
   
   Texto: "ELDOEHLWR" → Score: -12.8 (ainda baixo)
   ```

3. **Tentativa com chave [2, 0, 1]:**
   ```
   Ordem das colunas: [2, 0, 1]
   Grade:
   Col 0: H E L D
   Col 1: L W R
   Col 2: O E
   
   Lendo linha por linha: "HELLO WORLD"
   Score: 8.5 (alto! Contém n-gramas comuns do inglês)
   ```

4. **Resultado:** Chave `[2, 0, 1]` produz o texto `"HELLO WORLD"` com o maior score.

#### Passo 3: Avaliação com N-gramas

O scorer analisa sequências de 4 caracteres (quadgrams):
- `"HELL"` → frequência alta em inglês → score positivo
- `"ELLO"` → frequência alta → score positivo  
- `"WORL"` → frequência alta → score positivo
- `"ORLD"` → frequência alta → score positivo

Textos com n-gramas comuns do idioma recebem scores maiores, indicando que estão mais próximos do texto original.