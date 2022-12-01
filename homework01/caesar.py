def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
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


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
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
