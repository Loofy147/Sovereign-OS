import inspect
import importlib

class IndustrialSaturator:
    def __init__(self, torus):
        self.torus = torus

    def ingest_module(self, module_name):
        """Reflects and anchors public functions of a module into the Torus."""
        module = importlib.import_module(module_name)
        functions = inspect.getmembers(module, inspect.isfunction)

        for name, func in functions:
            if name.startswith('_'): continue

            try:
                source = inspect.getsource(func)
                identity = f"{module_name}.{name}"
                self.torus.ingest(identity, source)
                print(f"[SATURATOR] Anchored: {identity}")
            except Exception as e:
                print(f"[SATURATOR] Failed to anchor {name}: {e}")

    def ingest_function(self, identity, func):
        """Directly anchors a function object."""
        source = inspect.getsource(func)
        self.torus.ingest(identity, source)
        print(f"[SATURATOR] Anchored: {identity}")
