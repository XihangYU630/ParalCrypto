import numpy as np
from Crypto.Random import get_random_bytes
import os
import time
from Crypto.Cipher import AES

# # Your existing dummy_aes_encrypt_block function
# def dummy_aes_encrypt_block(block, key):
#     """
#     This is a placeholder for the block encryption function.
#     Replace this with an actual AES block encryption implementation.
#     """
#     return block  # This is just a dummy operation


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


# ECB mode encryption function
def ecb_mode_encrypt(data, key):
    block_size = 16  # Standard AES block size is 16 bytes
    num_blocks = (len(data) + block_size - 1) // block_size  # Calculate the number of blocks

    # Pad the data to ensure it is a multiple of the block size
    padded_data = data.ljust(num_blocks * block_size, b'\0')

    # Encrypt each block separately
    encrypted_data = b''.join([aes_encrypt_block(padded_data[i:i+block_size], key) for i in range(0, len(padded_data), block_size)])

    return encrypted_data

# ECB mode decryption function
def ecb_mode_decrypt(data, key):
    # Decryption in ECB mode is similar to encryption but with the decrypt operation
    block_size = 16  # Standard AES block size is 16 bytes
    num_blocks = len(data) // block_size

    # Decrypt each block separately
    decrypted_data = b''.join([aes_decrypt_block(data[i:i+block_size], key) for i in range(0, len(data), block_size)])

    return decrypted_data


if __name__ == '__main__':
    # Example usage
    key = get_random_bytes(32)  # AES-256 key

    original_image_path = '/Users/jimmyyu/Desktop/EECS475/paralcrypt/ECB/Lenna.png'
    decrypted_image_path = '/Users/jimmyyu/Desktop/EECS475/paralcrypt/ECB/Lenna_decrpt_paral.png'

    # Assuming data is loaded similarly to your CTR example
    with open(original_image_path, 'rb') as f:
        data = f.read()

    # Time ECB encryption
    start_time = time.time()
    encrypted_data = ecb_mode_encrypt(data, key)
    end_time = time.time()
    ecb_encrypt_time = end_time - start_time

    # Time ECB decryption
    start_time = time.time()
    decrypted_data = ecb_mode_decrypt(encrypted_data, key)
    end_time = time.time()
    ecb_decrypt_time = end_time - start_time

    with open(decrypted_image_path, 'wb') as f:
        f.write(decrypted_data)

    print("Paral ECB Encryption Time:", ecb_encrypt_time)
    print("Paral ECB Decryption Time:", ecb_decrypt_time)
