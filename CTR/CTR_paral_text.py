from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import time
import concurrent.futures

def encrypt(data, key, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cipher.encrypt(data)

def decrypt(encrypted_data, key, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cipher.decrypt(encrypted_data)

def parallel_encrypt(data_chunks, key, nonce):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(encrypt, chunk, key, nonce) for chunk in data_chunks]
        return [future.result() for future in concurrent.futures.as_completed(futures)]

def parallel_decrypt(encrypted_chunks, key, nonce):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(decrypt, chunk, key, nonce) for chunk in encrypted_chunks]
        return [future.result() for future in concurrent.futures.as_completed(futures)]

# Example usage
key = get_random_bytes(32)  # AES-256 key
nonce = get_random_bytes(8)  # Nonce for CTR mode should be half block size

data = b"Low Water Levels and Rising Temperatures: Recently, the Negro River in the Amazon rainforest near Manaus, Brazil, reached its lowest level in 120 years, dropping to just 12.70 meters. In Lake Tefe, located approximately 500 kilometers west, over 150 river dolphins were found dead, likely due to temperatures nearing 40 degrees"
data_chunks = [data[i:i+16] for i in range(0, len(data), 16)]  # 16-byte chunks

# Time parallel encryption
start_time = time.time()
encrypted_chunks_parallel = parallel_encrypt(data_chunks, key, nonce)
end_time = time.time()
parallel_encrypt_time = end_time - start_time

# Time parallel decryption
start_time = time.time()
decrypted_chunks_parallel = parallel_decrypt(encrypted_chunks_parallel, key, nonce)
end_time = time.time()
parallel_decrypt_time = end_time - start_time

print("Original:", data)
print("Decrypted:", b''.join(decrypted_chunks_parallel))
print("Parallel Encryption Time:", parallel_encrypt_time)
print("Parallel Decryption Time:", parallel_decrypt_time)
