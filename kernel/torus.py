import os
import hashlib
import numpy as np
from kernel.constants import DIM, T_SAFE, SHARD_CAP, BETA

class SovereignTorus:
    def __init__(self, dim=DIM, shard_cap=SHARD_CAP, memory_dir='./.assets'):
        self.dim = dim
        self.shard_cap = shard_cap
        self.memory_dir = memory_dir
        self.conf_thresh = T_SAFE
        self.beta = BETA

        os.makedirs(self.memory_dir, exist_ok=True)
        self.shards = []
        self._initialize_shards()

    def _initialize_shards(self):
        # Scan directory for existing shards
        shard_files = sorted([f for f in os.listdir(self.memory_dir) if f.startswith('shard_k_')])
        for f in shard_files:
            idx = f.split('_')[-1].split('.')[0]
            k_mat = np.load(os.path.join(self.memory_dir, f"shard_k_{idx}.npy"))
            v_mat = np.load(os.path.join(self.memory_dir, f"shard_v_{idx}.npy"))
            self.shards.append({'K': k_mat, 'V': v_mat, 'count': k_mat.shape[0]})

        if not self.shards:
            self._add_shard()

    def _add_shard(self):
        shard = {
            'K': np.zeros((0, self.dim), dtype=np.float32),
            'V': np.zeros((0, self.dim), dtype=np.float32),
            'count': 0
        }
        self.shards.append(shard)
        return shard

    def _generate_vec(self, label, salt="base:"):
        """Generates phase-locked unit vectors with namespace salting."""
        seed_str = f"{salt}{label}"
        h = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (2**32)
        rng = np.random.default_rng(h)
        vec = rng.standard_normal(self.dim).astype(np.float32)
        return vec / np.linalg.norm(vec)

    def ingest(self, identity, source_code):
        """Anchors a functional identity and its source into the manifold."""
        v_id = self._generate_vec(identity, salt="base:")
        v_src = self._generate_vec(source_code, salt="src:")

        current = self.shards[-1]
        if current['count'] >= self.shard_cap:
            current = self._add_shard()

        current['K'] = np.vstack([current['K'], v_id])
        current['V'] = np.vstack([current['V'], v_src])
        current['count'] += 1

        # Persistent backup
        idx = len(self.shards) - 1
        np.save(os.path.join(self.memory_dir, f"shard_k_{idx}.npy"), current['K'])
        np.save(os.path.join(self.memory_dir, f"shard_v_{idx}.npy"), current['V'])

        # Store source logic keyed by source vector hash
        h_src = hashlib.sha256(v_src.tobytes()).hexdigest()
        with open(os.path.join(self.memory_dir, f"logic_{h_src}.py"), 'w') as f:
            f.write(source_code)

    def retrieve(self, identity):
        """K-space Hopfield scan across shards for deterministic recall."""
        query_vec = self._generate_vec(identity, salt="base:")
        best_sim = -1.0
        target_v = None

        for shard in self.shards:
            if shard['count'] == 0: continue

            # Key-space nearest neighbor (Hopfield retrieval)
            similarities = shard['K'] @ query_vec
            idx = np.argmax(similarities)

            if similarities[idx] > best_sim:
                best_sim = similarities[idx]
                target_v = shard['V'][idx]

        if best_sim < self.conf_thresh:
            return None, best_sim

        return target_v, best_sim

    def fetch_source(self, v_src):
        h_src = hashlib.sha256(v_src.tobytes()).hexdigest()
        path = os.path.join(self.memory_dir, f"logic_{h_src}.py")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
        return None
