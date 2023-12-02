import numpy as np
from Crypto.Random import get_random_bytes
import os
import time
from Crypto.Cipher import AES
from concurrent.futures import ProcessPoolExecutor

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

####################
##### solution 1 ###
####################
def encrypt_block_wrapper(block_key_tuple):
    block, key = block_key_tuple
    return aes_encrypt_block(block, key)

def parallel_encrypt_blocks(blocks, key, block_size):
    with ProcessPoolExecutor() as executor:
        block_slices = [blocks[i:i+block_size] for i in range(0, len(blocks), block_size)]
        # Create a list of tuples for the map function
        block_key_pairs = [(block, key) for block in block_slices]
        # Map the encrypt_block_wrapper function over the block_key_pairs
        encrypted_blocks = executor.map(encrypt_block_wrapper, block_key_pairs)
    return b''.join(encrypted_blocks)



def ctr_mode_encrypt(data, key, nonce):
    if len(nonce) != 16:
        raise ValueError("Nonce must be 16 bytes long")

    data_length = len(data)
    block_size = 16
    num_blocks = (data_length + block_size - 1) // block_size  # Calculate the number of blocks

    # Split the nonce into two 64-bit parts
    nonce_upper = np.frombuffer(nonce[:8], dtype=np.uint64)
    nonce_lower = np.frombuffer(nonce[8:], dtype=np.uint64)

    # Generate counter values for the lower half
    counter_values_lower = (nonce_lower + np.arange(num_blocks, dtype=np.uint64)) 
    overflow = counter_values_lower < nonce_lower
    counter_values_upper = (nonce_upper + overflow)
    counter_blocks = np.vstack((counter_values_upper, counter_values_lower)).T.flatten()
    counter_blocks_bytes = counter_blocks.tobytes()


    ####################
    ##### solution 2 ###
    ####################
    # Encrypt counter blocks
    encrypted_counter_blocks = b''.join([aes_encrypt_block(counter_blocks_bytes[i:i+block_size], key) for i in range(0, len(counter_blocks_bytes), block_size)])

    ####################
    ##### solution 1 ###
    ####################
    # encrypted_counter_blocks = parallel_encrypt_blocks(counter_blocks_bytes, key, block_size)


    # XOR the encrypted counter blocks with data blocks
    encrypted_data = xor_bytes(data.ljust(num_blocks * block_size, b'\0'), encrypted_counter_blocks)[:data_length]

    return encrypted_data


def ctr_mode_decrypt(data, key, nonce):
    # Decryption in CTR mode is identical to encryption
    return ctr_mode_encrypt(data, key, nonce)

if __name__ == '__main__':



    # Example usage
    key = get_random_bytes(32)  # AES-256 key
    nonce = get_random_bytes(16)  # Nonce for CTR mode

    # data = b"Low Water Levels and Rising Temperatures: Recently, the Negro River in the Amazon rainforest near Manaus, Brazil, reached its lowest level in 120 years, dropping to just 12.70 meters. In Lake Tefe, located approximately 500 kilometers west, over 150 river dolphins were found dead, likely due to temperatures nearing 40 degrees"

    original_image_path = 'CTR/Lenna.png'
    decrypted_image_path = 'CTR/Lenna_decrpt_paral.png'

    with open(original_image_path, 'rb') as f:
        data = f.read()

    # Time parallel encryption
    start_time = time.time()
    encrypted_data = ctr_mode_encrypt(data, key, nonce)
    end_time = time.time()
    paral_encrypt_time = end_time - start_time

    # Time parallel decryption
    start_time = time.time()
    decrypted_data = ctr_mode_decrypt(encrypted_data, key, nonce)
    end_time = time.time()
    paral_decrypt_time = end_time - start_time

    with open(decrypted_image_path, 'wb') as f:
        f.write(decrypted_data)

    print("Paral Encryption Time:", paral_encrypt_time)
    print("Paral Decryption Time:", paral_decrypt_time)
