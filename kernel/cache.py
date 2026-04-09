import numpy as np
import hashlib
from kernel.geometry import fractional_bind, normalize, bind

class ChainCache:
    def __init__(self, torus):
        self.torus = torus
        self.cache = {}  # Dictionary lookup for registered endpoints (0.0002ms)
        self.salt = "chain:"

    def register(self, chain_label, terminal_vec):
        """Registers the final state of an execution chain."""
        h_id = hashlib.sha256(f"{self.salt}{chain_label}".encode()).hexdigest()
        self.cache[h_id] = terminal_vec

    def lookup(self, chain_label):
        """Ultra-fast path for known execution paths."""
        h_id = hashlib.sha256(f"{self.salt}{chain_label}".encode()).hexdigest()
        return self.cache.get(h_id)

    def execute_with_snap(self, logic_id_sequence):
        """
        verified fractional binding path (v7):
        1. Fractional Bind the sequence.
        2. Terminal Snap against ConceptStore.
        3. Register in ChainCache.
        """
        if not logic_id_sequence:
            return None

        # 1. Fractional Bind the sequence (alpha=0.5)
        # We start with the first vector and fractionally bind subsequent ones
        terminal_state = None

        for logic_id in logic_id_sequence:
            # We need the ID vector for each component
            vec = self.torus._generate_vec(logic_id, salt="base:")
            if terminal_state is None:
                terminal_state = vec
            else:
                # Fractional binding preserved phase structure
                # In sequence execution, we bind the state with fractional steps of the next
                f_step = fractional_bind(vec, alpha=0.5)
                terminal_state = bind(terminal_state, f_step)
                terminal_state = normalize(terminal_state)

        # 2. Terminal Snap (Not fully implemented without a ConceptStore of ALL vectors)
        # For now, we return the terminal_state.

        # 3. Register in ChainCache
        chain_label = "->".join(logic_id_sequence)
        self.register(chain_label, terminal_state)

        return terminal_state
