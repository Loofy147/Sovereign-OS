import os
import numpy as np
from kernel.torus import SovereignTorus

def run_scan():
    torus = SovereignTorus()
    all_keys = []
    for shard in torus.shards:
        if shard['count'] > 0:
            all_keys.append(shard['K'])

    if not all_keys:
        print("Manifold is empty.")
        return

    K_total = np.vstack(all_keys)
    num_keys = K_total.shape[0]

    if num_keys < 2:
        print(f"Manifold has {num_keys} keys. Scan skipped.")
        return

    # Calculate cosine similarity matrix
    # Since keys are unit vectors, this is just matrix multiplication
    sim_matrix = K_total @ K_total.T

    # Mask diagonal
    np.fill_diagonal(sim_matrix, 0)

    max_sim = np.max(sim_matrix)
    print(f"Manifold Health Check:")
    print(f"Total keys: {num_keys}")
    print(f"Max Cross-Similarity: {max_sim:.6f}")

    if max_sim > 0.094:
        print("WARNING: Manifold is Over-Saturated! Increase dimension or reduce shard_cap.")
    else:
        print("Manifold is HEALTHY.")

if __name__ == "__main__":
    run_scan()
