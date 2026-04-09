import numpy as np

def scan_manifold_integrity(torus):
    """
    Manifold Integrity Scan: Verifies that the Torus hasn't exceeded its geometric capacity.
    Flags 'Over-Saturation' if the Max Cross-Similarity between keys exceeds 0.094.
    """
    all_k = []
    for shard in torus.shards:
        if shard['K'].shape[0] > 0:
            all_k.append(shard['K'])

    if not all_k:
        return True, 0.0

    K = np.vstack(all_k)
    # Compute similarity matrix: N x N
    # Each row is already a unit vector
    sim_matrix = K @ K.T

    # Fill diagonal with zeros to ignore self-similarity
    np.fill_diagonal(sim_matrix, 0)

    max_sim = np.max(sim_matrix)

    # physical constant check (0.094 boundary)
    is_safe = max_sim <= 0.094

    return is_safe, max_sim
