import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

# AES ECB mode without IV

key = os.environ.get('CIPHER_PRIVATE_KEY')  # Must Be 16 char for AES128


def encrypt(raw):
    """
    Encrypt a raw string using AES encryption.

    This function takes a raw string as input and encrypts it using AES encryption with Electronic Codebook (ECB) mode.
    The input raw string is first padded to a multiple of 16 bytes to match the AES block size. The encryption key (named
    'key') is used to initialize the AES cipher. The encrypted data is then returned as a hexadecimal string.

    Parameters:
        raw (str): The raw string to be encrypted.

    Returns:
        str: The encrypted data as a hexadecimal string.

    Example Usage:
        plaintext = "Sensitive data to be encrypted."
        encrypted_data = encrypt(plaintext)
    """
    raw = pad(raw.encode(), 16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    encrypted_data = cipher.encrypt(raw)
    encrypted_data_hex = binascii.hexlify(encrypted_data).decode('utf-8')
    return encrypted_data_hex


def decrypt(enc):
    """
    Decrypt an AES-encrypted hexadecimal string.

    This function takes an AES-encrypted hexadecimal string as input and attempts to decrypt it using AES decryption with
    Electronic Codebook (ECB) mode. The input hexadecimal string is first converted back to bytes. The decryption key
    (named 'key') is used to initialize the AES cipher. The decrypted data is then un-padded, and the resulting raw string
    is returned.

    If decryption fails due to invalid input, incorrect padding, or any other error, the function returns None.

    Parameters:
        enc (str): The AES-encrypted data represented as a hexadecimal string.

    Returns:
        str or None: The decrypted raw string, or None if decryption fails.

    Example Usage:
        encrypted_hex = "f2a13e97248610da6a84e19cbef8324d"
        decrypted_data = decrypt(encrypted_hex)
    """
    try:
        enc = binascii.unhexlify(enc.encode('utf-8'))
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        decrypted = unpad(cipher.decrypt(enc), 16)
        return decrypted.decode('utf-8', 'ignore')
    except (ValueError, TypeError):
        # Handle decryption errors, such as invalid input or incorrect padding
        return None
