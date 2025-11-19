import math


def columnar_encrypt(plaintext: str, key: list[int]) -> str:
    plaintext = plaintext.upper().replace(" ", "")
    n_cols = len(key)
    n_rows = math.ceil(len(plaintext) / n_cols)

    grid = [[""] * n_cols for _ in range(n_rows)]

    idx = 0
    for row in range(n_rows):
        for col in range(n_cols):
            if idx < len(plaintext):
                grid[row][col] = plaintext[idx]
                idx += 1

    ciphertext = []
    for col_order in sorted(range(n_cols), key=lambda x: key[x]):
        for row in range(n_rows):
            if grid[row][col_order]:
                ciphertext.append(grid[row][col_order])

    return "".join(ciphertext)


def substitution_encrypt(plaintext: str, mapping: dict[str, str]) -> str:
    result = []
    for c in plaintext.upper():
        if c.isalpha():
            result.append(mapping.get(c, c))
        else:
            result.append(c)
    return "".join(result)


# Suas frases
texts = [
    "BY ENDURANCE WE CONQUER",
    "BE LIKE WATER",
    "GODS OF DEATH LOVES APPLES",
    "SCOOBY DOOBY DOO",
]

# Chaves de permutação (tamanho 5)
perm_keys = [[3, 1, 4, 0, 2], [2, 0, 4, 1, 3], [1, 3, 0, 4, 2], [4, 2, 1, 3, 0]]

# Mapeamentos de substituição
sub_mappings = [
    {
        "A": "Q",
        "B": "W",
        "C": "E",
        "D": "R",
        "E": "T",
        "F": "Y",
        "G": "U",
        "H": "I",
        "I": "O",
        "J": "P",
        "K": "A",
        "L": "S",
        "M": "D",
        "N": "F",
        "O": "G",
        "P": "H",
        "Q": "J",
        "R": "K",
        "S": "L",
        "T": "Z",
        "U": "X",
        "V": "C",
        "W": "V",
        "X": "B",
        "Y": "N",
        "Z": "M",
    },
    {
        "A": "M",
        "B": "N",
        "C": "B",
        "D": "V",
        "E": "C",
        "F": "X",
        "G": "Z",
        "H": "A",
        "I": "S",
        "J": "D",
        "K": "F",
        "L": "G",
        "M": "H",
        "N": "J",
        "O": "K",
        "P": "L",
        "Q": "P",
        "R": "O",
        "S": "I",
        "T": "U",
        "U": "Y",
        "V": "T",
        "W": "R",
        "X": "E",
        "Y": "W",
        "Z": "Q",
    },
    {
        "A": "Z",
        "B": "X",
        "C": "C",
        "D": "V",
        "E": "B",
        "F": "N",
        "G": "M",
        "H": "A",
        "I": "S",
        "J": "D",
        "K": "F",
        "L": "G",
        "M": "H",
        "N": "J",
        "O": "K",
        "P": "L",
        "Q": "P",
        "R": "Q",
        "S": "W",
        "T": "Y",
        "U": "U",
        "V": "I",
        "W": "E",
        "X": "R",
        "Y": "T",
        "Z": "O",
    },
    {
        "A": "L",
        "B": "M",
        "C": "N",
        "D": "B",
        "E": "V",
        "F": "C",
        "G": "X",
        "H": "Z",
        "I": "A",
        "J": "S",
        "K": "D",
        "L": "F",
        "M": "G",
        "N": "H",
        "O": "J",
        "P": "K",
        "Q": "P",
        "R": "Q",
        "S": "W",
        "T": "Y",
        "U": "U",
        "V": "I",
        "W": "E",
        "X": "R",
        "Y": "T",
        "Z": "O",
    },
]

# Gerar permutações
for i, (text, key) in enumerate(zip(texts, perm_keys), 1):
    ciphertext = columnar_encrypt(text, key)
    filename = f"data/ciphertexts/permutation_0{i}.txt"
    with open(filename, "w") as f:
        f.write(ciphertext)
    print(f"{filename}: {ciphertext}")
    print(f"  Key: {key}\n")

# Gerar substituições
for i, (text, mapping) in enumerate(zip(texts, sub_mappings), 1):
    ciphertext = substitution_encrypt(text, mapping)
    filename = f"data/ciphertexts/substitution_0{i}.txt"
    with open(filename, "w") as f:
        f.write(ciphertext)
    print(f"{filename}: {ciphertext}")
    print(f"  Mapping sample: {dict(list(mapping.items())[:10])}\n")
