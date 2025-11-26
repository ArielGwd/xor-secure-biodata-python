import base64

def xor_encrypt(text: str, key: str) -> str:
    
    if text is None:
        return None
    
    cipher_bytes = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(text)])
    return base64.b64encode(cipher_bytes).decode()

def xor_decrypt(encoded_cipher: str, key: str) -> str:
    if encoded_cipher is None:
        return None
    
    cipher_bytes = base64.b64decode(encoded_cipher)
    original_chars = [chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(cipher_bytes)]
    return ''.join(original_chars)
