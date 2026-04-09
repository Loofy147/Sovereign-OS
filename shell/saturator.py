import inspect
import importlib
from kernel.torus import SovereignTorus

class IndustrialSaturator:
    def __init__(self, torus):
        self.torus = torus

    def saturate_package(self, package_name):
        """Reflects a package and anchors all public functions into the Torus."""
        try:
            pkg = importlib.import_module(package_name)
            for name, obj in inspect.getmembers(pkg):
                if inspect.isfunction(obj) and not name.startswith('_'):
                    try:
                        source = inspect.getsource(obj)
                        identity = f"{package_name}.{name}"
                        self.torus.ingest(identity, source)
                        print(f"Anchored: {identity}")
                    except (TypeError, OSError):
                        # Some functions might not have source available (e.g. built-ins)
                        continue
        except Exception as e:
            print(f"Saturation Failure [{package_name}]: {e}")
