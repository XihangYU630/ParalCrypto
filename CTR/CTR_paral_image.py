from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from concurrent.futures import ThreadPoolExecutor
import os
import time

def parallel_encrypt(data_chunks, key, nonce):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(lambda p: cipher.encryptor().update(p), chunk) for chunk in data_chunks]
        encrypted_chunks = [future.result() for future in futures]
    return b''.join(encrypted_chunks) + cipher.encryptor().finalize()

def parallel_decrypt(encrypted_chunks, key, nonce):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(lambda p: cipher.decryptor().update(p), chunk) for chunk in encrypted_chunks]
        decrypted_chunks = [future.result() for future in futures]
    return b''.join(decrypted_chunks) + cipher.decryptor().finalize()

def process_image_parallel(file_path, output_path, key, nonce, mode='encrypt'):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Split data into chunks for parallel processing
    chunk_size = 1024 # Adjust the size based on your requirements
    data_chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    if mode == 'encrypt':
        processed_data = parallel_encrypt(data_chunks, key, nonce)
    else:
        processed_data = parallel_decrypt(data_chunks, key, nonce)

    with open(output_path, 'wb') as f:
        f.write(processed_data)

# Example usage
key = os.urandom(32) # AES-256 key
nonce = os.urandom(16) # Nonce for CTR mode

original_image_path = '/Users/jimmyyu/Desktop/EECS475/ParalCrypto/Lenna.png'
encrypted_image_path = '/Users/jimmyyu/Desktop/EECS475/ParalCrypto/image.enc'
decrypted_image_path = '/Users/jimmyyu/Desktop/EECS475/ParalCrypto/Lenna_decrpt.png'

# Encrypt the image in parallel
start_time = time.time()
process_image_parallel(original_image_path, encrypted_image_path, key, nonce, mode='encrypt')
end_time = time.time()
encrypt_time = end_time - start_time

# Decrypt the image in parallel
start_time = time.time()
process_image_parallel(encrypted_image_path, decrypted_image_path, key, nonce, mode='decrypt')
end_time = time.time()
decrypt_time = end_time - start_time


print("parallel Encryption Time:", encrypt_time)
print("parallel Decryption Time:", decrypt_time)