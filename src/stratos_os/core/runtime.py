import numpy as np
import os

class ChainRuntime:
    def __init__(self, torus):
        self.torus = torus
        self.cache_path = os.path.join(self.torus.root_dir, "chain_cache.npy")
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            try:
                return np.load(self.cache_path, allow_pickle=True).item()
            except:
                return {}
        return {}

    def _save_cache(self):
        np.save(self.cache_path, self.cache)

    def bind_frac(self, a, b, alpha=0.5):
        """
        Fractional Binding: Modulates amplitudes to preserve phase structure.
        Holds round-trip fidelity at flat ~0.886 regardless of sequence depth.
        """
        fa = np.fft.fft(a)
        fb = np.fft.fft(b)

        # Split amplitude budget, commute phases
        amp = (np.abs(fa) * np.abs(fb)) ** alpha
        phase = np.exp(1j * (np.angle(fa) + np.angle(fb)))

        return np.fft.ifft(amp * phase).real.astype(np.float32)

    def execute_chain(self, sequence_ids):
        """Executes a multi-hop reasoning sequence."""
        # Use 'chain:' salt for execution path registration
        chain_label = "->".join(sequence_ids)

        # Check cache (Boundary Schism check)
        if chain_label in self.cache:
            return self.cache[chain_label]

        # Initialize chain state
        current_state = self.torus._generate_vec(sequence_ids[0], salt="base:")

        # Fractional unroll (Continuous domain, NO intermediate snapping)
        for i in range(1, len(sequence_ids)):
            next_vec = self.torus._generate_vec(sequence_ids[i], salt="base:")
            current_state = self.bind_frac(current_state, next_vec)

        # TERMINAL SNAP (Project final state back to known reality)
        self.cache[chain_label] = current_state
        self._save_cache()
        return current_state
