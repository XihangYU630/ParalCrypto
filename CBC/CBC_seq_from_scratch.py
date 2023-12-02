from Crypto.Random import get_random_bytes
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def xor_bytes(a, b):
    """
    XOR two byte strings.
    """
    return bytes(x ^ y for x, y in zip(a, b))

def cbc_mode_encrypt(data, key, iv):
    block_size = 16  # AES block size is 16 bytes
    encrypted = b''
    prev_ciphertext = iv

    # Pad the data to ensure it is a multiple of the block size
    padded_data = pad(data, block_size)

    for i in range(0, len(padded_data), block_size):
        block = padded_data[i:i+block_size]
        
        # XOR the block with the previous ciphertext
        block = xor_bytes(block, prev_ciphertext)
        
        # Encrypt the block
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_block = cipher.encrypt(block)
        
        encrypted += encrypted_block
        prev_ciphertext = encrypted_block

    return encrypted

def cbc_mode_decrypt(data, key, iv):
    block_size = 16  # AES block size is 16 bytes
    decrypted = b''
    prev_ciphertext = iv
    cipher = AES.new(key, AES.MODE_ECB)

    for i in range(0, len(data), block_size):
        current_ciphertext = data[i:i+block_size]
        decrypted_block = cipher.decrypt(current_ciphertext)
        decrypted_block = xor_bytes(decrypted_block, prev_ciphertext)
        decrypted += decrypted_block
        prev_ciphertext = current_ciphertext

    decrypted = unpad(decrypted, block_size)
    
    return decrypted

if __name__ == '__main__':
    # Example usage
    key = get_random_bytes(32)  # AES-256 key
    iv = get_random_bytes(16)   # Initialization vector for CBC mode


    original_image_path = 'CBC/Lenna.png'
    decrypted_image_path = 'CBC/Lenna_decrpt_seq.png'

    with open(original_image_path, 'rb') as f:
        data = f.read()


    num_runs = 50
    total_time_encypt = 0
    total_time_decypt = 0

    for _ in range(num_runs):

        # Time sequential CBC encryption
        start_time = time.time()
        encrypted_data = cbc_mode_encrypt(data, key, iv)
        end_time = time.time()
        seq_encrypt_time = end_time - start_time

        # Time sequential CBC decryption
        start_time = time.time()
        decrypted_data = cbc_mode_decrypt(encrypted_data, key, iv)
        end_time = time.time()
        seq_decrypt_time = end_time - start_time

        total_time_encypt += seq_encrypt_time
        total_time_decypt += seq_decrypt_time

    average_time_encrypt = total_time_encypt / num_runs
    average_time_decrypt = total_time_decypt / num_runs


    with open(decrypted_image_path, 'wb') as f:
        f.write(decrypted_data)

    print("Sequential CBC Encryption Time:", average_time_encrypt)
    print("Sequential CBC Decryption Time:", average_time_decrypt)
