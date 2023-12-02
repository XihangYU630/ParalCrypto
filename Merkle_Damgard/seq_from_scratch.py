from Crypto.Hash import SHA256
import time

def hash_block(block):
    """
    Hash a block of data using SHA256.
    """
    hasher = SHA256.new()
    hasher.update(block)
    return hasher.digest()

def merkle_damgard(data, block_size=64):
    """
    Sequential Merkle-Damgård construction.
    """
    # Split the data into blocks
    num_blocks = len(data) // block_size + (1 if len(data) % block_size else 0)
    blocks = [data[i*block_size:(i+1)*block_size] for i in range(num_blocks)]

    # Process each block sequentially
    hashed_blocks = [hash_block(block) for block in blocks]

    # Combine the hashed results
    combined_hash = SHA256.new()
    for h in hashed_blocks:
        combined_hash.update(h)
    
    return combined_hash.digest()

# Example usage
if __name__ == '__main__':
    data = b"Your data here"  # Using a large dataset for more noticeable timing

    # Time the Merkle-Damgård construction
    start_time = time.time()
    final_hash = merkle_damgard(data)
    end_time = time.time()
    merkle_damgard_creation_time = end_time - start_time

    print("Merkle-Damgard Creation Time:", merkle_damgard_creation_time)
    print("Final Hash:", final_hash.hex())
