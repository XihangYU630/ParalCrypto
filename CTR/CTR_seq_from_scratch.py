from Crypto.Random import get_random_bytes
import os
import time
import numpy as np
from Crypto.Cipher import AES


def aes_encrypt_block(block, key):
    """
    Encrypts a single block of data using AES.
    """
    # Ensure the block is the correct size for AES (16 bytes)
    if len(block) != 16:
        raise ValueError("Block must be 16 bytes long")

    # Create a new AES cipher object with ECB mode (as we're encrypting a single block)
    cipher = AES.new(key, AES.MODE_ECB)

    # Encrypt the block
    encrypted_block = cipher.encrypt(block)

    return encrypted_block

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def ctr_mode_encrypt(data, key, nonce):
    if len(nonce) != 16:
        raise ValueError("Nonce must be 16 bytes long")

    data_length = len(data)
    block_size = 16
    num_blocks = (data_length + block_size - 1) // block_size  # Calculate the number of blocks

    # Split the nonce into two 64-bit parts
    nonce_upper = np.frombuffer(nonce[:8], dtype=np.uint64)
    nonce_lower = np.frombuffer(nonce[8:], dtype=np.uint64)

    encrypted_data = b''

    for i in range(num_blocks):
        # Increment the lower part of the counter
        counter_block_lower = nonce_lower + i

        # Handle overflow
        counter_block_upper = nonce_upper + (counter_block_lower < nonce_lower)

        # Combine the upper and lower parts of the counter block
        counter_block = np.concatenate((counter_block_upper, counter_block_lower)).tobytes()

        # Encrypt the counter block
        encrypted_counter_block = aes_encrypt_block(counter_block, key)

        # XOR the encrypted counter block with the data block
        data_block = data[i*block_size : (i+1)*block_size].ljust(block_size, b'\0')
        encrypted_block = xor_bytes(data_block, encrypted_counter_block[:len(data_block)])
        encrypted_data += encrypted_block

    return encrypted_data


def ctr_mode_decrypt(data, key, nonce):
    # Decryption in CTR mode is identical to encryption
    return ctr_mode_encrypt(data, key, nonce)


if __name__ == '__main__':
    # Example usage
    key = get_random_bytes(32)  # AES-256 key
    nonce = get_random_bytes(16)  # Nonce for CTR mode

    data = b"Low Water Levels and Rising Temperatures: Recently, the Negro River in the Amazon rainforest near Manaus, Brazil, reached its lowest level in 120 years, dropping to just 12.70 meters. In Lake Tefe, located approximately 500 kilometers west, over 150 river dolphins were found dead, likely due to temperatures nearing 40 degrees"


    # original_image_path = 'CTR/Lenna.png'
    # decrypted_image_path = 'CTR/Lenna_decrpt_seq.png'

    # with open(original_image_path, 'rb') as f:
    #     data = f.read()


    # Time parallel encryption
    start_time = time.time()
    encrypted_data = ctr_mode_encrypt(data, key, nonce)
    end_time = time.time()
    seq_encrypt_time = end_time - start_time

    # Time parallel decryption
    start_time = time.time()
    decrypted_data = ctr_mode_decrypt(encrypted_data, key, nonce)
    end_time = time.time()
    seq_decrypt_time = end_time - start_time

    # with open(decrypted_image_path, 'wb') as f:
    #     f.write(decrypted_data)

    # print("Original:", data)
    # print("Encrypted:", encrypted_data)
    # print("Decrypted:", decrypted_data)
    print("seq Encryption Time:", seq_encrypt_time)
    print("seq Decryption Time:", seq_decrypt_time)
