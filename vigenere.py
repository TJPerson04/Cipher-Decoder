ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def encode_vig(text: str, key: str) -> str:
    '''
    Encode given text using the classic vigenere cipher.\n

    text: The plaintext to encode.\n
    key: The key to use in the cipher.
    '''
    for character in key:
        if (not character in ALPHABET):
            return text
    if len(key) == 0:
        return text

    text = text.lower()

    key_index = 0
    output = ""

    for i in range(len(text)):
        if (not text[i] in ALPHABET):
            output += text[i]
            continue

        start = ALPHABET.index(text[i])
        offset = ALPHABET.index(key[key_index])

        output += ALPHABET[(start + offset) % len(ALPHABET)]

        key_index += 1
        key_index %= len(key)
    
    return output

def decode_vig(text: str, key: str) -> str:
    '''
    Decode the given text using the classic vigenere cipher.\n

    text: The ciphertext to decode.\n
    key: The key to use in the cipher.
    '''
    for character in key:
        if (not character in ALPHABET):
            return text
    if len(key) == 0:
        return text

    text = text.lower()

    key_index = 0
    output = ""

    for i in range(len(text)):
        if (not text[i] in ALPHABET):
            output += text[i]
            continue

        start = ALPHABET.index(text[i])
        offset = ALPHABET.index(key[key_index])

        output += ALPHABET[(len(ALPHABET) + start - offset) % len(ALPHABET)]

        key_index += 1
        key_index %= len(key)
    
    return output

def reverse_vig(plaintext: str, ciphertext: str) -> str:
    '''
    Find the key that brings the given plaintext to the given ciphertext.
    '''
    if (len(plaintext) != len(ciphertext)):
        return ""
    
    key = ""
    for i in range(len(plaintext)):
        plain_letter = plaintext[i]
        cipher_letter = ciphertext[i]

        index = len(ALPHABET) - (ALPHABET.index(plain_letter) - ALPHABET.index(cipher_letter))
        index %= len(ALPHABET)

        key += ALPHABET[index]
    
    return key


def decode_beaufort(text: str, key: str) -> str:
    '''
    Decode the given text using the beaufort style of vigenere cipher.\n

    text: The ciphertext to decode.\n
    key: The key to use in the cipher.
    '''
    for character in key:
        if (not character in ALPHABET):
            return text
        
    if len(key) == 0:
        return text

    text = text.lower()

    key_index = 0
    output = ""

    for i in range(len(text)):
        if (not text[i] in ALPHABET):
            output += text[i]
            continue

        start = ALPHABET.index(text[i])
        offset = ALPHABET.index(key[key_index])

        output += ALPHABET[(len(ALPHABET) - start + offset) % len(ALPHABET)]

        key_index += 1
        key_index %= len(key)
    
    return output

def encode_variant_beaufort(text: str, key: str) -> str:
    '''
    Encode the given text using the variant beaufort style of vigenere cipher.\n

    text: The plaintext to encode.\n
    key: The key to use in the cipher.
    '''
    for character in key:
        if (not character in ALPHABET):
            return text
        
    if len(key) == 0:
        return text

    text = text.lower()

    key_index = 0
    output = ""

    for i in range(len(text)):
        if (not text[i] in ALPHABET):
            output += text[i]
            continue

        start = ALPHABET.index(text[i])
        offset = ALPHABET.index(key[key_index])

        output += ALPHABET[(len(ALPHABET) + start - offset) % len(ALPHABET)]

        key_index += 1
        key_index %= len(key)
    
    return output

def decode_variant_beaufort(text: str, key: str) -> str:
    '''
    Decode the given text using the variant beaufort style of vigenere cipher.\n

    text: The ciphertext to decode.\n
    key: The key to use in the cipher.
    '''
    for character in key:
        if (not character in ALPHABET):
            return text
        
    if len(key) == 0:
        return text

    text = text.lower()

    key_index = 0
    output = ""

    for i in range(len(text)):
        if (not text[i] in ALPHABET):
            output += text[i]
            continue

        start = ALPHABET.index(text[i])
        offset = ALPHABET.index(key[key_index])

        output += ALPHABET[(start + offset) % len(ALPHABET)]

        key_index += 1
        key_index %= len(key)
    
    return output