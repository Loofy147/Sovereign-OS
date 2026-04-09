import sys
import types
import hashlib
import importlib.abc
import importlib.machinery
import os

class SovereignLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, torus):
        self.torus = torus

    def find_spec(self, fullname, path, target=None):
        # Intercept any import starting with 'stratos'
        if fullname == 'stratos' or fullname.startswith('stratos.'):
            return importlib.machinery.ModuleSpec(fullname, self)
        return None

    def create_module(self, spec):
        # Create an empty namespace in RAM
        module = types.ModuleType(spec.name)
        if spec.name == 'stratos' or spec.name.endswith('.'): # Package-like
             module.__path__ = []
        return module

    def exec_module(self, module):
        if module.__name__ == 'stratos':
            return

        # Extract the logical identity (e.g., stratos.neural_gate -> neural_gate)
        logic_id = module.__name__.split('stratos.', 1)[1]
        if logic_id.startswith('.'):
            logic_id = logic_id[1:]

        # Route through K-Space Hopfield
        v_val, confidence = self.torus.retrieve(logic_id)

        if v_val is not None:
            # Hash the value vector to find the binary blob on disk
            blob_hash = hashlib.md5(v_val.tobytes()).hexdigest()
            blob_path = os.path.join(self.torus.root_dir, f"blob_{blob_hash}.bin")

            try:
                with open(blob_path, 'rb') as f:
                    source_code = f.read().decode('utf-8')

                # Execute logic directly into the blank RAM module
                exec(source_code, module.__dict__)
            except FileNotFoundError:
                raise ImportError(f"CRITICAL: Trace found but binary logic blob missing for {logic_id}")
        else:
            # If it's a sub-package (not a leaf logic), we might want to allow it?
            # But the logic says it routes through K-Space.
            # Maybe it's a sub-package if it doesn't have a blob?
            # The current implementation expects every 'stratos.*' to be a logic blob.
            # But 'stratos.sys.echo' implies 'stratos.sys' is a package and 'echo' is the logic?
            # Or 'sys.echo' is the logic identity.

            # If I import stratos.sys.echo, first 'stratos' is imported, then 'stratos.sys', then 'stratos.sys.echo'.
            # 'stratos.sys' would be retrieved with identity 'sys'.
            # 'stratos.sys.echo' would be retrieved with identity 'sys.echo'.

            # Let's see how ingest was called: os_kernel.ingest("sys.echo", ...)
            # So 'stratos.sys.echo' should work if 'sys.echo' is in Torus.
            # What about 'stratos.sys'? It probably fails T_safe.

            # We should probably treat it as a package if it fails T_safe but could be a prefix?
            # Or just set __path__ to make it a package.
            module.__path__ = []
            # We don't raise ImportError yet, because it might be a parent package.
            # However, if we are at the leaf and it's not found, it will fail later when used?
            # Actually, 'import stratos.sys.echo as echo' will fail if 'stratos.sys' fails to be imported.

            # Let's try to be more flexible.
            pass

def boot_stratos():
    from core.manifold import SovereignTorus

    torus = SovereignTorus()
    sys.meta_path.insert(0, SovereignLoader(torus))
    print("[STRATOS] Sovereign Manifold Booted. Import interception active.")
    return torus
