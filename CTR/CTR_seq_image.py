from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from concurrent.futures import ThreadPoolExecutor
import os
import time

def sequential_encrypt(data, key, nonce):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

def sequential_decrypt(encrypted_data, key, nonce):
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()

def process_image_sequential(file_path, output_path, key, nonce, mode='encrypt'):
    with open(file_path, 'rb') as f:
        data = f.read()

    if mode == 'encrypt':
        processed_data = sequential_encrypt(data, key, nonce)
    else:
        processed_data = sequential_decrypt(data, key, nonce)

    with open(output_path, 'wb') as f:
        f.write(processed_data)

# Example usage
key = os.urandom(32) # AES-256 key
nonce = os.urandom(16) # Nonce for CTR mode

original_image_path = '/Users/jimmyyu/Desktop/EECS475/paralcrypt/Lenna.png'
encrypted_image_path = '/Users/jimmyyu/Desktop/EECS475/paralcrypt/image.enc'
decrypted_image_path = '/Users/jimmyyu/Desktop/EECS475/paralcrypt/Lenna_decrpt.png'

# Example usage
# Encrypt the image sequentially
start_time = time.time()
process_image_sequential(original_image_path, encrypted_image_path, key, nonce, mode='encrypt')
end_time = time.time()
encrypt_time = end_time - start_time

# Decrypt the image sequentially
start_time = time.time()
process_image_sequential(encrypted_image_path, decrypted_image_path, key, nonce, mode='decrypt')
end_time = time.time()
decrypt_time = end_time - start_time


print("Sequential Encryption Time:", encrypt_time)
print("Sequential Decryption Time:", decrypt_time)
