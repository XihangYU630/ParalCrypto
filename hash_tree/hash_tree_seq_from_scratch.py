from Crypto.Hash import SHA256
import numpy as np
import time
import os

def hash_block(block):
    """Hashes a single block."""
    hasher = SHA256.new()
    hasher.update(block)
    return hasher.digest()

def create_merkle_tree_sequential(data, block_size=32):
    num_blocks = (len(data) + block_size - 1) // block_size
    padded_data = data.ljust(num_blocks * block_size, b'\0')
    
    # Reshape the data into blocks using the same method as in the vectorized version
    np_data = np.frombuffer(padded_data, dtype=f'S{block_size}')

    # Hash the leaf nodes
    leaf_nodes = [hash_block(block) for block in np_data]

    # Sequentially combine and hash to create parent nodes
    while len(leaf_nodes) > 1:
        temp_nodes = []
        for i in range(0, len(leaf_nodes), 2):
            left = leaf_nodes[i]
            right = leaf_nodes[i + 1] if i + 1 < len(leaf_nodes) else left
            combined = hash_block(np.char.add(np.array([left]), np.array([right]))[0])
            temp_nodes.append(combined)
        leaf_nodes = temp_nodes

    return leaf_nodes[0]

if __name__ == '__main__':

    # data = b"Low Water Levels and Rising Temperatures: Recently, the Negro River in the Amazon rainforest near Manaus, Brazil, reached its lowest level in 120 years, dropping to just 12.70 meters. In Lake Tefe, located approximately 500 kilometers west, over 150 river dolphins were found dead, likely due to temperatures nearing 40 degrees"

    original_image_path = 'hash_tree/Lenna.png'

    # Assuming data is loaded similarly to your CTR example
    with open(original_image_path, 'rb') as f:
        data = f.read()

    num_runs = 50
    total_time = 0

    for _ in range(num_runs):
        start_time = time.time()
        root_hash = create_merkle_tree_sequential(data)
        end_time = time.time()
        merkle_tree_creation_time = end_time - start_time
        total_time += merkle_tree_creation_time

    average_time = total_time / num_runs

    print(f"Average Sequential Merkle Tree Creation Time for {num_runs} runs:", average_time)
    print("Root Hash:", root_hash.hex())