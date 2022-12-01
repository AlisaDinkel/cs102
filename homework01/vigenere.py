def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key = keyword
    while len(key) < len(plaintext):
        key += keyword

    for i in range(0, len(plaintext)):
        char = plaintext[i]
        if key[i].isupper():
            shift = ord(key[i]) - ord("A")
        elif key[i].islower():
            shift = ord(key[i]) - ord("a")

        if char.isupper():
            if ord("A") <= ord(char) + shift <= ord("Z"):
                new_ord = ord(char) + shift
            else:
                new_ord = ord(char) - 26 + shift
            new_char = chr(new_ord)
            ciphertext += new_char
        elif char.islower():
            if ord("a") <= ord(char) + shift <= ord("z"):
                new_ord = ord(char) + shift
            else:
                new_ord = ord(char) - 26 + shift
            new_char = chr(new_ord)
            ciphertext += new_char
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key = keyword
    while len(key) < len(ciphertext):
        key += keyword

    for i in range(0, len(ciphertext)):
        char = ciphertext[i]
        if key[i].isupper():
            shift = ord(key[i]) - ord("A")
        elif key[i].islower():
            shift = ord(key[i]) - ord("a")

        if char.isupper():
            if ord("A") <= ord(char) - shift <= ord("Z"):
                new_ord = ord(char) - shift
            else:
                new_ord = ord(char) + 26 - shift
            new_char = chr(new_ord)
            plaintext += new_char
        elif char.islower():
            if ord("a") <= ord(char) - shift <= ord("z"):
                new_ord = ord(char) - shift
            else:
                new_ord = ord(char) + 26 - shift
            new_char = chr(new_ord)
            plaintext += new_char
        else:
            plaintext += char
    return plaintext
