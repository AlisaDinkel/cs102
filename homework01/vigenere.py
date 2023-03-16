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
    key = keyword.lower()
    while len(key) < len(plaintext):
        key += keyword.lower()

    for i in range(0, len(plaintext)):
        char = plaintext[i]
        shift = ord(key[i]) - ord("a")
        if char.isupper():
            char_index = ord(char) - ord("A")
            new_ord = (char_index + shift) % 26 + ord("A")
            ciphertext += chr(new_ord)
        elif char.islower():
            char_index = ord(char) - ord("a")
            new_ord = (char_index + shift) % 26 + ord("a")
            ciphertext += chr(new_ord)
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
    key = keyword.lower()
    while len(key) < len(ciphertext):
        key += keyword.lower()

    for i in range(0, len(ciphertext)):
        char = ciphertext[i]
        shift = ord(key[i]) - ord("a")
        if char.isupper():
            char_index = ord(char) - ord("A")
            new_ord = (char_index - shift) % 26 + ord("A")
            plaintext += chr(new_ord)
        elif char.islower():
            char_index = ord(char) - ord("a")
            new_ord = (char_index - shift) % 26 + ord("a")
            plaintext += chr(new_ord)
        else:
            plaintext += char
    return plaintext
