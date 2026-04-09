import sys
import types
import importlib.abc
import importlib.machinery

class SovereignLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, torus):
        self.torus = torus

    def find_spec(self, fullname, path, target=None):
        if fullname == 'sovereign' or fullname.startswith('sovereign.'):
            return importlib.machinery.ModuleSpec(fullname, self, is_package=True)
        return None

    def create_module(self, spec):
        return types.ModuleType(spec.name)

    def exec_module(self, module):
        if module.__name__ == 'sovereign':
            return

        # Extract logic key: sovereign.network.ping -> network.ping
        logic_id = module.__name__.split('sovereign.', 1)[1]

        v_src, confidence = self.torus.retrieve(logic_id)

        if v_src is not None:
            source = self.torus.fetch_source(v_src)
            if source:
                # Execute in the module's blank namespace
                exec(source, module.__dict__)
            else:
                raise ImportError(f"Source lost for logical identity: {logic_id}")
        else:
            # We don't raise here to allow intermediate packages (namespaces)
            # like 'sovereign.core' when 'sovereign.core.signal' is the target.
            pass

def initialize():
    from kernel import SovereignTorus
    torus = SovereignTorus()
    sys.meta_path.insert(0, SovereignLoader(torus))
    return torus
