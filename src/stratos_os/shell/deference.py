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
        if fullname == 'stratos' or fullname.startswith('stratos.'):
            return importlib.machinery.ModuleSpec(fullname, self)
        return None

    def create_module(self, spec):
        module = types.ModuleType(spec.name)
        if spec.name == 'stratos' or spec.name.endswith('.'):
            module.__path__ = []
        return module

    def exec_module(self, module):
        if module.__name__ == 'stratos':
            return

        logic_id = module.__name__.split('stratos.', 1)[1]
        if logic_id.startswith('.'):
            logic_id = logic_id[1:]

        # Attempt to retrieve direct logic (e.g., stratos.json.loads)
        v_val, confidence = self.torus.retrieve(logic_id)

        if v_val is not None:
            self._inject_logic(module, logic_id, v_val)
        else:
            # Mark as package to allow sub-module imports
            module.__path__ = []

    def _inject_logic(self, module, logic_id, v_val):
        blob_hash = hashlib.md5(v_val.tobytes()).hexdigest()
        blob_path = os.path.join(self.torus.root_dir, f"blob_{blob_hash}.bin")

        try:
            with open(blob_path, 'rb') as f:
                source_code = f.read().decode('utf-8')
            exec(source_code, module.__dict__)
        except FileNotFoundError:
            msg = f"CRITICAL: Trace found but binary logic blob missing for {logic_id} at {blob_path}"
            raise ImportError(msg)


def boot_stratos():
    from stratos_os.core.manifold import SovereignTorus

    torus = SovereignTorus()
    sys.meta_path.insert(0, SovereignLoader(torus))
    print("[STRATOS] Sovereign Manifold Booted. Import interception active.")
    return torus
