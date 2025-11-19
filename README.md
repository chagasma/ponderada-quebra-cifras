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

## Algoritmo de Quebra de Cifra de Substituição (Monoalfabética)

### Visão Geral

O algoritmo de quebra de cifra de substituição implementado neste projeto quebra cifras de substituição monoalfabéticas, onde cada letra do alfabeto é substituída por outra letra de forma consistente. Este tipo de cifra mantém a estrutura do texto original, apenas trocando os caracteres.

### Como é Realizada a Quebra

A quebra da cifra segue os seguintes passos:

1. **Análise de Frequências Inicial**: O algoritmo calcula a frequência de cada letra no texto cifrado e compara com as frequências esperadas do idioma inglês.

2. **Criação do Mapeamento Inicial**: Cria um mapeamento inicial onde as letras mais frequentes do texto cifrado são mapeadas para as letras mais frequentes do inglês (E, T, A, O, I, N, S, H, R, D, L, C, U, M, W, F, G, Y, P, B, V, K, J, X, Q, Z).

3. **Otimização com Hill Climbing**: Melhora o mapeamento inicial usando a técnica de hill climbing:
   - Testa trocas de pares de letras no mapeamento
   - Se o score melhorar, aceita a troca
   - Repete o processo por milhares de iterações

4. **Múltiplos Restarts**: Para evitar ficar preso em mínimos locais, o algoritmo executa múltiplas tentativas (padrão: 10) com diferentes mapeamentos iniciais aleatórios.

5. **Avaliação da Qualidade**: Cada tentativa é avaliada usando um scorer baseado em n-gramas (quadgrams), que calcula a probabilidade do texto decifrado ser inglês válido.

6. **Seleção da Melhor Solução**: O mapeamento que produz o texto com maior score é retornado como resultado.

### Lógica do Código

#### 1. Função `_initial_mapping(ciphertext)`

Cria um mapeamento inicial baseado em análise de frequências:

```python
def _initial_mapping(self, ciphertext: str) -> Dict[str, str]:
```

**Passos:**

- Conta a frequência de cada letra no texto cifrado
- Ordena as letras do texto cifrado por frequência (mais frequente primeiro)
- Mapeia cada letra cifrada para a letra correspondente na ordem de frequência do inglês
- Para letras não encontradas no texto, atribui mapeamentos aleatórios disponíveis

**Exemplo:**

```
Texto cifrado: "XBMF XBMF" (onde X é mais frequente que B, M, F)
Ordem de frequência do inglês: "ETAOINSHRDLCUMWFGYPBVKJXQZ"

Mapeamento inicial:
X → E (mais frequente no cifrado → mais frequente no inglês)
B → T
M → A
F → O
```

#### 2. Função `_decrypt(ciphertext, mapping)`

Aplica o mapeamento para descriptografar o texto:

```python
def _decrypt(self, ciphertext: str, mapping: Dict[str, str]) -> str:
```

**Passos:**

- Para cada caractere no texto cifrado:
  - Se for uma letra, substitui pelo valor do mapeamento
  - Se não for letra (espaços, pontuação), mantém inalterado
- Retorna o texto descriptografado

**Exemplo:**

```
Texto cifrado: "XBMF"
Mapeamento: {'X': 'H', 'B': 'E', 'M': 'L', 'F': 'O'}
Resultado: "HELO"
```

#### 3. Função `_hill_climb(ciphertext, mapping, iterations)`

Otimiza o mapeamento usando hill climbing:

```python
def _hill_climb(self, ciphertext: str, mapping: Dict[str, str], iterations: int = 10000) -> Tuple[Dict[str, str], str]:
```

**Algoritmo:**

1. Inicializa o melhor mapeamento com o mapeamento fornecido
2. Para cada iteração (padrão: 10.000):
   - Seleciona aleatoriamente duas letras do alfabeto (ex: 'A' e 'B')
   - Troca seus valores no mapeamento (se A→X e B→Y, vira A→Y e B→X)
   - Descriptografa o texto com o novo mapeamento
   - Calcula o score do texto descriptografado
   - Se o score melhorou, mantém a troca e atualiza o melhor mapeamento
   - Se o score piorou, desfaz a troca (reverte para o estado anterior)
3. Retorna o melhor mapeamento encontrado e o texto descriptografado

**Por que funciona:** O hill climbing explora o espaço de soluções fazendo pequenas modificações (trocas de pares) e mantendo apenas as que melhoram o resultado. Isso permite refinar gradualmente o mapeamento inicial baseado em frequências.

#### 4. Função `break_cipher(ciphertext, iterations, num_restarts)`

Função principal que orquestra a quebra:

```python
def break_cipher(self, ciphertext: str, iterations: int = 50000, num_restarts: int = 10) -> Tuple[str, Dict[str, str]]:
```

**Estratégia:**

1. **Primeira tentativa com mapeamento baseado em frequências:**
   - Cria mapeamento inicial usando `_initial_mapping`
   - Otimiza com hill climbing
   - Armazena como melhor resultado inicial

2. **Múltiplos restarts (padrão: 9 tentativas adicionais):**
   - Para cada restart:
     - Cria um mapeamento completamente aleatório
     - Otimiza com hill climbing
     - Se o resultado for melhor que o atual, atualiza o melhor resultado

3. **Retorno:** Retorna o melhor texto descriptografado e o melhor mapeamento encontrado

**Por que múltiplos restarts:** O hill climbing pode ficar preso em mínimos locais (soluções boas, mas não ótimas). Executar múltiplas tentativas com diferentes pontos de partida aumenta significativamente a chance de encontrar a solução correta.

### Exemplo Simples

Vamos quebrar a cifra passo a passo com um exemplo:

**Texto original:** `"HELLO WORLD"`  
**Mapeamento usado na cifragem:** `{'H': 'X', 'E': 'B', 'L': 'M', 'O': 'F', 'W': 'Q', 'R': 'P', 'D': 'K'}`

#### Passo 1: Cifragem (como o texto foi cifrado originalmente)

```
Texto original: "HELLO WORLD"
Aplicando mapeamento:
H → X
E → B
L → M
O → F
W → Q
R → P
D → K

Texto cifrado: "XBMFM FQPMK"
```

#### Passo 2: Análise de Frequências Inicial

**Frequências no texto cifrado:**

```
M: 3 ocorrências (30%)
B: 1 ocorrência (10%)
F: 2 ocorrências (20%)
X: 1 ocorrência (10%)
Q: 1 ocorrência (10%)
P: 1 ocorrência (10%)
K: 1 ocorrência (10%)
```

**Ordem de frequência no cifrado:** `M, F, B, X, Q, P, K, ...`

**Ordem de frequência no inglês:** `E, T, A, O, I, N, S, H, R, D, L, C, U, M, W, F, G, Y, P, B, V, K, J, X, Q, Z`

#### Passo 3: Criação do Mapeamento Inicial

```
Mapeamento baseado em frequências:
M → E (mais frequente no cifrado → mais frequente no inglês)
F → T
B → A
X → O
Q → I
P → N
K → S
...
```

**Tentativa de descriptografia:**

```
Texto cifrado: "XBMFM FQPMK"
Aplicando mapeamento inicial:
X → O
B → A
M → E
F → T
Q → I
P → N
K → S

Resultado: "OAEET ITNES" → Score: -8.3 (baixo, não faz sentido)
```

#### Passo 4: Otimização com Hill Climbing

**Iteração 1:**

- Troca: M ↔ F (M→E vira M→T, F→T vira F→E)
- Novo mapeamento: `{..., 'M': 'T', 'F': 'E', ...}`
- Texto: "OAEET ETNES" → Score: -7.1 (melhorou!)
- **Aceita a troca**

**Iteração 2:**

- Troca: B ↔ X (B→A vira B→O, X→O vira X→A)
- Novo mapeamento: `{..., 'B': 'O', 'X': 'A', ...}`
- Texto: "OAEET ETNES" → Score: -7.5 (piorou)
- **Rejeita a troca** (reverte)

**Iteração 3:**

- Troca: X ↔ M (X→O vira X→T, M→T vira M→O)
- Novo mapeamento: `{..., 'X': 'T', 'M': 'O', ...}`
- Texto: "OAEET ETNES" → Score: -6.8 (melhorou!)
- **Aceita a troca**

**... (continua por 10.000 iterações) ...**

**Após otimização:**

```
Mapeamento otimizado:
X → H
B → E
M → L
F → O
Q → W
P → R
K → D
...
```

**Resultado:** "HELLO WORLD" → Score: 12.4 (alto! Texto válido em inglês)

#### Passo 5: Múltiplos Restarts

O algoritmo executa mais 9 tentativas com mapeamentos iniciais aleatórios:

- **Restart 1:** Mapeamento aleatório → Hill climbing → Score: 8.2
- **Restart 2:** Mapeamento aleatório → Hill climbing → Score: 5.1
- **Restart 3:** Mapeamento aleatório → Hill climbing → Score: 12.4 (igual ao melhor!)
- **... (continua até 10 tentativas no total) ...**

O melhor resultado encontrado (Score: 12.4) é retornado.

#### Passo 6: Avaliação com N-gramas

O scorer analisa sequências de 4 caracteres (quadgrams) no texto descriptografado:

- `"HELL"` → frequência muito alta em inglês → score muito positivo
- `"ELLO"` → frequência alta → score positivo
- `"WORL"` → frequência alta → score positivo
- `"ORLD"` → frequência alta → score positivo

Textos com n-gramas comuns do idioma recebem scores maiores, confirmando que a descriptografia está correta.

### Comparação: Mapeamento Inicial vs. Otimizado

| Letra Cifrada | Mapeamento Inicial (Freq) | Mapeamento Otimizado (Hill Climb) | Correto |
|---------------|---------------------------|-----------------------------------|---------|
| X             | O                         | H                                 | ✓       |
| B             | A                         | E                                 | ✓       |
| M             | E                         | L                                 | ✓       |
| F             | T                         | O                                 | ✓       |
| Q             | I                         | W                                 | ✓       |
| P             | N                         | R                                 | ✓       |
| K             | S                         | D                                 | ✓       |

O mapeamento inicial baseado apenas em frequências acerta algumas letras, mas o hill climbing refina e corrige os erros, chegando ao mapeamento completo e correto.
