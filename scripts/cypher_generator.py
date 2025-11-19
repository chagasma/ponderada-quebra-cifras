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


perm_texts = [
    "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",  # THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG
    "DEFENDTHEEASTWALLOFTHECASTLE",  # DEFEND THE EAST WALL OF THE CASTLE
    "MEETMEATTHESTATION",  # MEET ME AT THE STATION
    "SENDREINFORCEMENTSIMMEDIATELY",  # SEND REINFORCEMENTS IMMEDIATELY
]

sub_texts = [
    "THECRYPTOGRAPHYISTHESCIENCEOFPROTECTINGINFORMATIONBYTRANSFORMINGITINTOANUNREADABLEFORMATCALLEDCIPHERTEXTONLYTHOSEWHOPOSSESEACRETKEYCANDECIPHER",  # THE CRYPTOGRAPHY IS THE SCIENCE OF PROTECTING INFORMATION BY TRANSFORMING IT INTO AN UNREADABLE FORMAT CALLED CIPHERTEXT ONLY THOSE WHO POSSESS A SECRET KEY CAN DECIPHER
    "INTHEWORLDOFSECURITYANDPRIVACYENCRYPTIONPLAYSAVITALROLEBYENSURINGTHATDATAREMAINSSAFEFROMUNAUTHORIZEDACCESSEVENIFINTERCEPTEDDURINGTRANSMISSION",  # IN THE WORLD OF SECURITY AND PRIVACY ENCRYPTION PLAYS A VITAL ROLE BY ENSURING THAT DATA REMAINS SAFE FROM UNAUTHORIZED ACCESS EVEN IF INTERCEPTED DURING TRANSMISSION
    "MODERNENCRYPTIONALGORITHMSSUCHASTHERSAMDAESPROVIDESTRONGPROTECTIONAGAINSTBRUTEFORCEATTTACKSMAKINGITPRACTICALLYIMPOSSIBLETOBREAKTHECODE",  # MODERN ENCRYPTION ALGORITHMS SUCH AS THE RSA MD AES PROVIDE STRONG PROTECTION AGAINST BRUTE FORCE ATTACKS MAKING IT PRACTICALLY IMPOSSIBLE TO BREAK THE CODE
    "CRYPTANALYSISISTHEARTANDSCIENCEOFBREAKINGCIPHERSWITHOUTKNOWINGTHEKEYEXPERTSUSEVARIOUSTECHNIQUESINCLUDINGFREQUENCYANALYSISANDPATTERNRECOGNITION",  # CRYPTANALYSIS IS THE ART AND SCIENCE OF BREAKING CIPHERS WITHOUT KNOWING THE KEY EXPERTS USE VARIOUS TECHNIQUES INCLUDING FREQUENCY ANALYSIS AND PATTERN RECOGNITION
]

perm_keys = [[3, 1, 4, 0, 2], [2, 0, 4, 1, 3], [1, 3, 0, 4, 2], [4, 2, 1, 3, 0]]

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

print("=" * 80)
print("GERANDO CIFRAS DE PERMUTAÇÃO")
print("=" * 80)
for i, (text, key) in enumerate(zip(perm_texts, perm_keys), 1):
    ciphertext = columnar_encrypt(text, key)
    filename = f"data/ciphertexts/permutation_0{i}.txt"
    with open(filename, "w") as f:
        f.write(ciphertext)
    print(f"\n{filename}:")
    print(f"  Plaintext:  {text[:60]}...")
    print(f"  Ciphertext: {ciphertext[:60]}...")
    print(f"  Key: {key}")

print("\n" + "=" * 80)
print("GERANDO CIFRAS DE SUBSTITUIÇÃO")
print("=" * 80)
for i, (text, mapping) in enumerate(zip(sub_texts, sub_mappings), 1):
    ciphertext = substitution_encrypt(text, mapping)
    filename = f"data/ciphertexts/substitution_0{i}.txt"
    with open(filename, "w") as f:
        f.write(ciphertext)
    print(f"\n{filename}:")
    print(f"  Plaintext:  {text[:60]}...")
    print(f"  Ciphertext: {ciphertext[:60]}...")
    print(f"  Text length: {len(text)} chars")
    print(f"  Mapping sample: {dict(list(mapping.items())[:5])}...")
