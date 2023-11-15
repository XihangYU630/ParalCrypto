from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import time

def encrypt(data, key, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cipher.encrypt(data)

def decrypt(encrypted_data, key, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cipher.decrypt(encrypted_data)

def sequential_encrypt(data_chunks, key, nonce):
    encrypted_chunks = []
    for chunk in data_chunks:
        encrypted_chunks.append(encrypt(chunk, key, nonce))
    return encrypted_chunks

def sequential_decrypt(encrypted_chunks, key, nonce):
    decrypted_chunks = []
    for chunk in encrypted_chunks:
        decrypted_chunks.append(decrypt(chunk, key, nonce))
    return decrypted_chunks

# Example usage
key = get_random_bytes(32)  # AES-256 key
nonce = get_random_bytes(8)  # Nonce for CTR mode should be half block size

data = b"Low Water Levels and Rising Temperatures: Recently, the Negro River in the Amazon rainforest near Manaus, Brazil, reached its lowest level in 120 years, dropping to just 12.70 meters. In Lake Tefe, located approximately 500 kilometers west, over 150 river dolphins were found dead, likely due to temperatures nearing 40 degrees"
data_chunks = [data[i:i+16] for i in range(0, len(data), 16)]

# Time sequential encryption
start_time = time.time()
encrypted_chunks_sequential = sequential_encrypt(data_chunks, key, nonce)
end_time = time.time()
sequential_encrypt_time = end_time - start_time

# Time sequential decryption
start_time = time.time()
decrypted_chunks_sequential = sequential_decrypt(encrypted_chunks_sequential, key, nonce)
end_time = time.time()
sequential_decrypt_time = end_time - start_time

print("Original:", data)
print("Decrypted:", b''.join(decrypted_chunks_sequential))
print("Sequential Encryption Time:", sequential_encrypt_time)
print("Sequential Decryption Time:", sequential_decrypt_time)
