from Crypto.Hash import SHA256
import numpy as np
import time
import os

def hash_blocks(blocks):
    """Hashes a batch of blocks."""
    hashed_blocks = []
    for block in blocks:
        hasher = SHA256.new()
        hasher.update(block)
        hashed_blocks.append(hasher.digest())
    return hashed_blocks

def create_merkle_tree_vectorized(data, block_size=32, batch_size=8192):
    num_blocks = (len(data) + block_size - 1) // block_size
    padded_data = data.ljust(num_blocks * block_size, b'\0')
    
    # Reshape the data into blocks
    np_data = np.frombuffer(padded_data, dtype=f'S{block_size}')
    
    # Hash the leaf nodes in batches
    leaf_nodes = []
    for i in range(0, len(np_data), batch_size):
        batch = np_data[i:i + batch_size]
        leaf_nodes.extend(hash_blocks(batch))
    
    # Sequentially combine and hash to create parent nodes
    while len(leaf_nodes) > 1:
        # Convert leaf nodes to numpy array for vectorization
        leaf_nodes_np = np.array(leaf_nodes)
        if len(leaf_nodes_np) % 2 != 0:
            leaf_nodes_np = np.append(leaf_nodes_np, leaf_nodes_np[-1])
        leaf_nodes_np = leaf_nodes_np.reshape(-1, 2)
        combined_blocks = np.char.add(leaf_nodes_np[:, 0], leaf_nodes_np[:, 1])

        # Process combined blocks in batches
        temp_nodes = []
        for i in range(0, len(combined_blocks), batch_size):
            batch = combined_blocks[i:i + batch_size]
            temp_nodes.extend(hash_blocks(batch))

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
        root_hash = create_merkle_tree_vectorized(data)
        end_time = time.time()
        merkle_tree_creation_time = end_time - start_time
        total_time += merkle_tree_creation_time

    average_time = total_time / num_runs

    print(f"Average Pararllel Merkle Tree Creation Time for {num_runs} runs:", average_time)
    print("Root Hash:", root_hash.hex())