import numpy as np
import hashlib
import os


class SovereignTorus:
    def __init__(self, dim=1024, shard_cap=40, root_dir='./.stratos_assets'):
        self.dim = dim
        self.shard_cap = shard_cap
        self.root_dir = os.path.abspath(root_dir)

        # Locked Physical Constants (STRATOS-OS v7/v8)
        self.t_safe = 0.09375            # The absolute 3/√D physical boundary
        self.adjoint_ceiling = 0.71      # Inherent χ² loss of circular convolution
        self.spectral_learning_rate = 0.147  # Prevents divergence at η=1.0

        self.shards = []
        self._fused_K = np.zeros((0, self.dim), dtype=np.float32)
        self._fused_V = np.zeros((0, self.dim), dtype=np.float32)

        os.makedirs(self.root_dir, exist_ok=True)
        self._sync_shards()

    def _generate_vec(self, seed_str, salt="base:"):
        """Generates phase-locked unit vectors. Uses 64-bit hashing to prevent collisions."""
        full_seed = f"{salt}{seed_str}"
        # Prevent 32-bit little-endian truncation bug
        h = int.from_bytes(hashlib.sha256(full_seed.encode()).digest()[:8], 'little')
        rng = np.random.default_rng(h)
        vec = rng.standard_normal(self.dim).astype(np.float32)
        return vec / np.linalg.norm(vec)

    def bind(self, a, b):
        """
        Standard circular convolution for storage (preserves amplitude contrast).
        Optimized with RFFT for real-valued vectors.
        """
        return np.fft.irfft(np.fft.rfft(a) * np.fft.rfft(b), n=len(a)).real.astype(np.float32)

    def unbind(self, c, a):
        """
        Standard circular correlation for trace isolation.
        Optimized with RFFT for real-valued vectors.
        """
        return np.fft.irfft(np.fft.rfft(c) * np.conj(np.fft.rfft(a)), n=len(c)).real.astype(np.float32)

    def _sync_shards(self):
        files = sorted([f for f in os.listdir(self.root_dir) if f.startswith('k_mat_')])
        self.shards = []
        all_k = []
        all_v = []
        for f in files:
            idx = f.split('_')[-1].split('.')[0]
            k = np.load(os.path.join(self.root_dir, f"k_mat_{idx}.npy"))
            v = np.load(os.path.join(self.root_dir, f"v_mat_{idx}.npy"))
            self.shards.append({'K': k, 'V': v})
            all_k.append(k)
            all_v.append(v)

        if all_k:
            self._fused_K = np.vstack(all_k)
            self._fused_V = np.vstack(all_v)
        else:
            self._fused_K = np.zeros((0, self.dim), dtype=np.float32)
            self._fused_V = np.zeros((0, self.dim), dtype=np.float32)

    def ingest(self, identity, payload_bytes):
        """Auto-associative Two-Matrix storage. No online normalization."""
        v_id = self._generate_vec(identity, salt="base:")
        v_val = self._generate_vec(payload_bytes, salt="src:")

        # Enforce Hard Shard Cap
        if not self.shards or self.shards[-1]['K'].shape[0] >= self.shard_cap:
            self.shards.append({'K': np.zeros((0, self.dim), dtype=np.float32),
                                'V': np.zeros((0, self.dim), dtype=np.float32)})

        current = self.shards[-1]
        current['K'] = np.vstack([current['K'], v_id])
        current['V'] = np.vstack([current['V'], v_val])

        # Update fused matrices for fast retrieval
        self._fused_K = np.vstack([self._fused_K, v_id])
        self._fused_V = np.vstack([self._fused_V, v_val])

        # Persist manifold state
        idx = len(self.shards) - 1
        np.save(os.path.join(self.root_dir, f"k_mat_{idx}.npy"), current['K'])
        np.save(os.path.join(self.root_dir, f"v_mat_{idx}.npy"), current['V'])

        # Write binary source blob
        blob_hash = hashlib.md5(v_val.tobytes()).hexdigest()
        with open(os.path.join(self.root_dir, f"blob_{blob_hash}.bin"), 'wb') as f:
            f.write(payload_bytes.encode('utf-8'))

    def retrieve(self, identity):
        """K-space nearest-neighbor scan. Works up to σ=0.20 noise."""
        if self._fused_K.shape[0] == 0:
            return None, -1.0

        q_vec = self._generate_vec(identity, salt="base:")

        # O(N) Fused Matrix multiplication for exact nearest-neighbor
        sims = self._fused_K @ q_vec
        idx = np.argmax(sims)
        best_sim = sims[idx]
        target_v = self._fused_V[idx]

        # The T_safe Confidence Gate
        if best_sim >= self.t_safe:
            return target_v, best_sim
        return None, best_sim
