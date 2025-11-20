"""
Cipher generator for creating test ciphertexts.
Generates both substitution and permutation ciphers.
"""

import math
import random
import string


def columnar_encrypt(plaintext: str, key: list[int]) -> str:
    """Encrypt text using columnar transposition."""
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
    """Encrypt text using monoalphabetic substitution."""
    result = []
    for c in plaintext.upper():
        if c.isalpha():
            result.append(mapping.get(c, c))
        else:
            result.append(c)
    return "".join(result)


def generate_random_substitution() -> dict[str, str]:
    """Generate a random substitution mapping."""
    alphabet = list(string.ascii_uppercase)
    shuffled = alphabet.copy()
    random.shuffle(shuffled)
    return {a: s for a, s in zip(alphabet, shuffled)}


# Plaintext samples for permutation ciphers
perm_texts = [
    "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",
    "DEFENDTHEEASTWALLOFTHECASTLE",
    "MEETMEATTHESTATION",
    "SENDREINFORCEMENTSIMMEDIATELY",
    "ATTACKATDAWN",
    "THETREASUREISBEHINDTHEWATERFALL",
    "RENDEZVOUSATMIDNIGHT",
    "OPERATIONSUCCESSFUL",
    "RETREATTOTHENORTHERNBORDER",
    "ALLUNITSADVANCETOPOSITION",
]

# Plaintext samples for substitution ciphers
sub_texts = [
    "THECRYPTOGRAPHYISTHESCIENCEOFPROTECTINGINFORMATIONBYTRANSFORMINGITINTOANUNREADABLEFORMATCALLEDCIPHERTEXTONLYTHOSEWHOPOSSESEACRETKEYCANDECIPHER",
    "INTHEWORLDOFSECURITYANDPRIVACYENCRYPTIONPLAYSAVITALROLEBYENSURINGTHATDATAREMAINSSAFEFROMUNAUTHORIZEDACCESSEVENIFINTERCEPTEDDURINGTRANSMISSION",
    "MODERNENCRYPTIONALGORITHMSSUCHASTHERSAMDAESPROVIDESTRONGPROTECTIONAGAINSTBRUTEFORCEATTTACKSMAKINGITPRACTICALLYIMPOSSIBLETOBREAKTHECODE",
    "CRYPTANALYSISISTHEARTANDSCIENCEOFBREAKINGCIPHERSWITHOUTKNOWINGTHEKEYEXPERTSUSEVARIOUSTECHNIQUESINCLUDINGFREQUENCYANALYSISANDPATTERNRECOGNITION",
    "THESTUDYOFCRYPTOGRAPHYINVOLVESMATHEMATICSCOMPUTERSCIENCEANDELECTRICALENGINEERINGTODESIGNSECURECOMMUNICATIONSYSTEMSTHATPROTECTSENSITIVEDATA",
    "HISTORICALLYCRYPTOGRAPHYWASUSEDBYMILITARIESANDGOVERNMENTSTOPROTECTSECRETMESSAGESFROMBEINGINTERCEPTEDBYENEMIESDURINGWARTIMECOMMUNICATIONS",
    "PUBLICKEYCRYPTOGRAPHYREVOLUTIONIZEDTHEFIELDBYALLOWINGSECURECOMMUNICATIONWITHOUTTHEEEDTONEXCHANGESECRETKEYSBEFOREHANDMAKINGONLINESECURITYPOSSIBLE",
    "DIGITALSIГNATURESPROVIDEASECUREWAYOFVERIFYINGTHEAUTHENTICITYANDINTEGRITYOFDIGITALDOCUMENTSUSINGCRYPTOGRAPHICTECHNIQUESBASEDONPUBLICKEYSYSTEMS",
    "QUANTUMCRYPTOGRAPHYISANEMERGINGFIELDTHATLEVERAGESTHEPROPERTIESOFQUANTUMMECHANICSTOCREATECOMMUNICATIONSYSTEMSTHATARETHEORETICALLYSECUREAGAINSTEAVESDROPPING",
    "BLOCKCIPHERSPROCESSDATAINBLOCKSOFDETERMINEDSIZERATHERTHANINDIVIDUALCHARACTERSPROVIDINGSTRONGERENCRYPTIONFORMODERNCOMPUTERAPPLICATIONSSUCHASSECUREFILETORAGE",
]

# Keys for permutation ciphers (5 columns)
perm_keys = [
    [3, 1, 4, 0, 2],
    [2, 0, 4, 1, 3],
    [1, 3, 0, 4, 2],
    [4, 2, 1, 3, 0],
    [0, 3, 2, 4, 1],
    [2, 4, 0, 3, 1],
    [4, 1, 3, 0, 2],
    [1, 0, 4, 2, 3],
    [3, 2, 1, 0, 4],
    [0, 2, 4, 1, 3],
]


def main():
    """Generate all cipher samples."""
    print("=" * 80)
    print("GENERATING PERMUTATION CIPHERS")
    print("=" * 80)

    for i, (text, key) in enumerate(zip(perm_texts, perm_keys), 1):
        ciphertext = columnar_encrypt(text, key)
        filename = f"data/ciphertexts/permutation_{i:02d}.txt"
        with open(filename, "w") as f:
            f.write(ciphertext)
        print(f"\n{filename}:")
        print(f"  Plaintext:  {text[:60]}...")
        print(f"  Ciphertext: {ciphertext[:60]}...")
        print(f"  Key: {key}")

    print("\n" + "=" * 80)
    print("GENERATING SUBSTITUTION CIPHERS")
    print("=" * 80)

    for i, text in enumerate(sub_texts, 1):
        mapping = generate_random_substitution()
        ciphertext = substitution_encrypt(text, mapping)
        filename = f"data/ciphertexts/substitution_{i:02d}.txt"
        with open(filename, "w") as f:
            f.write(ciphertext)
        print(f"\n{filename}:")
        print(f"  Plaintext:  {text[:60]}...")
        print(f"  Ciphertext: {ciphertext[:60]}...")
        print(f"  Text length: {len(text)} chars")
        print(f"  Mapping sample: {dict(list(mapping.items())[:5])}...")

    print("\n" + "=" * 80)
    print(f"Generated {len(perm_texts)} permutation and {len(sub_texts)} substitution ciphers")
    print("=" * 80)


if __name__ == "__main__":
    main()
