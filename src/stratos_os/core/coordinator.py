import os
from stratos_os.core.manifold import SovereignTorus
from stratos_os.core.runtime import ChainRuntime

class TGICoordinator:
    """
    Multi-Agent TGI Coordinator: Manages isolated manifolds for different reasoning roles.
    - Base: Permanent foundational logic
    - Chain: Execution results and trace paths
    - Proof: Formal verification results
    """
    def __init__(self, root_dir='./.stratos_assets'):
        self.root_dir = root_dir

        # Isolated Manifolds
        self.base = SovereignTorus(root_dir=os.path.join(root_dir, 'base'))
        self.chain = SovereignTorus(root_dir=os.path.join(root_dir, 'chain'))
        self.proof = SovereignTorus(root_dir=os.path.join(root_dir, 'proof'))

        # Runtimes
        self.runtimes = {
            'base': ChainRuntime(self.base),
            'chain': ChainRuntime(self.chain),
            'proof': ChainRuntime(self.proof)
        }

    def route_query(self, identity):
        """Cross-manifold routing via confidence-gated scans."""
        results = []
        for name, manifold in [('base', self.base), ('chain', self.chain), ('proof', self.proof)]:
            v, sim = manifold.retrieve(identity)
            results.append((sim, name, v))

        # Sort by confidence
        results.sort(key=lambda x: x[0], reverse=True)
        best_sim, best_manifold, best_v = results[0]

        if best_sim >= self.base.t_safe:
            return best_manifold, best_v, best_sim
        return None, None, best_sim

    def register_execution(self, sequence_ids):
        """Executes in base, stores result in chain manifold."""
        result_vec = self.runtimes['base'].execute_chain(sequence_ids)
        chain_label = "->".join(sequence_ids)
        # Store the high-level trace in the chain manifold
        self.chain.ingest(chain_label, chain_label) # Using label as payload for trace identification
        return result_vec
