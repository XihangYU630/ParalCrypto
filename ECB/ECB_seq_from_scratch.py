from Crypto.Random import get_random_bytes
import os
import time
from Crypto.Cipher import AES

def aes_encrypt_block(block, key):
    """
    Encrypts a single 16-byte block of data using AES.
    """
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(block)

def aes_decrypt_block(block, key):
    """
    Decrypts a single 16-byte block of data using AES.
    """
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(block)

def ecb_mode_encrypt(data, key):
    block_size = 16  # AES block size is 16 bytes
    encrypted = b''

    # Pad the data to ensure it is a multiple of the block size
    padded_data = data.ljust((len(data) + block_size - 1) // block_size * block_size, b'\0')

    for i in range(0, len(padded_data), block_size):
        block = padded_data[i:i+block_size]

        # Encrypt the block
        encrypted_block = aes_encrypt_block(block, key)
        encrypted += encrypted_block

    return encrypted

def ecb_mode_decrypt(data, key):
    block_size = 16  # AES block size is 16 bytes
    decrypted = b''

    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]

        # Decrypt the block (assuming symmetric encryption/decryption)
        decrypted_block = aes_decrypt_block(block, key)
        decrypted += decrypted_block

    return decrypted

# Example usage
key = get_random_bytes(32)  # AES-256 key

# Assuming data is loaded similarly to your CTR example
original_image_path = '/Users/jimmyyu/Desktop/EECS475/paralcrypt/ECB/Lenna.png'
decrypted_image_path = '/Users/jimmyyu/Desktop/EECS475/paralcrypt/ECB/Lenna_decrpt_seq.png'

with open(original_image_path, 'rb') as f:
    data = f.read()

# Time sequential ECB encryption
start_time = time.time()
encrypted_data = ecb_mode_encrypt(data, key)
end_time = time.time()
seq_encrypt_time = end_time - start_time

# Time sequential ECB decryption
start_time = time.time()
decrypted_data = ecb_mode_decrypt(encrypted_data, key)
end_time = time.time()
seq_decrypt_time = end_time - start_time

with open(decrypted_image_path, 'wb') as f:
    f.write(decrypted_data)

# print("Original:", data)
# print("Encrypted:", encrypted_data)
# print("Decrypted:", decrypted_data)
print("Sequential ECB Encryption Time:", seq_encrypt_time)
print("Sequential ECB Decryption Time:", seq_decrypt_time)
