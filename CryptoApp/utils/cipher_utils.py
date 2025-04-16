import random
import string
import base64

def vigenere_encrypt(text, key):
    """
    Encrypt text using Vigenère cipher
    
    Args:
        text (str): Text to encrypt
        key (str): Encryption key
        
    Returns:
        str: Encrypted text
    """
    if not text or not key:
        return None
        
    text = text.upper()
    key = key.upper()
    
    key = ''.join(c for c in key if c.isalpha())
    
    if not key:
        return None
    
    key = key * (len(text) // len(key) + 1)
    key = key[:len(text)]
    
    encrypted = []
    for i in range(len(text)):
        if text[i].isalpha():
            text_num = ord(text[i]) - ord('A')
            key_num = ord(key[i]) - ord('A')
            encrypted_num = (text_num + key_num) % 26
            encrypted.append(chr(encrypted_num + ord('A')))
        else:
            encrypted.append(text[i])
            
    return ''.join(encrypted)

def vigenere_decrypt(text, key):
    """
    Decrypt text using Vigenère cipher
    
    Args:
        text (str): Text to decrypt
        key (str): Decryption key
        
    Returns:
        str: Decrypted text
    """
    if not text or not key:
        return None
        
    text = text.upper()
    key = key.upper()
    
    key = ''.join(c for c in key if c.isalpha())
    
    if not key:
        return None
    
    key = key * (len(text) // len(key) + 1)
    key = key[:len(text)]
    
    decrypted = []
    for i in range(len(text)):
        if text[i].isalpha():
            text_num = ord(text[i]) - ord('A')
            key_num = ord(key[i]) - ord('A')
            decrypted_num = (text_num - key_num) % 26
            decrypted.append(chr(decrypted_num + ord('A')))
        else:
            decrypted.append(text[i])
            
    return ''.join(decrypted)

def generate_vigenere_key(length=None):
    """
    Generate a random key for Vigenère cipher
    
    Args:
        length (int, optional): Length of the key. If None, a random length between 3 and 8 will be used.
        
    Returns:
        str: Random key consisting of uppercase letters
    """
    if length is None:
        length = random.randint(3, 8)
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def one_time_pad_encrypt(text):
    """
    Encrypt text using a one-time pad and return both the ciphertext and key
    
    Args:
        text (str): Text to encrypt
        
    Returns:
        tuple: (encrypted_text, key) where encrypted_text is base64-encoded ciphertext and key is bytes
    """
    if not text:
        return None, None
        
    text_bytes = text.encode('utf-8')
    key = bytes(random.randint(0, 255) for _ in range(len(text_bytes)))
    
    encrypted_bytes = bytes(a ^ b for a, b in zip(text_bytes, key))
    encrypted_text = base64.b64encode(encrypted_bytes).decode('utf-8')
    
    return encrypted_text, key

def one_time_pad_decrypt(encrypted_text, key):
    """
    Decrypt text using a one-time pad
    
    Args:
        encrypted_text (str): Base64-encoded encrypted text
        key (bytes): Decryption key
        
    Returns:
        str: Decrypted text
    """
    if not encrypted_text or not key:
        return None
    
    try:
        encrypted_bytes = base64.b64decode(encrypted_text)
        
        if len(key) < len(encrypted_bytes):
            return None
            
        decrypted_bytes = bytes(a ^ b for a, b in zip(encrypted_bytes, key))
        return decrypted_bytes.decode('utf-8')
    except Exception:
        return None 