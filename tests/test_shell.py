import pytest
import os
import shutil
import sys
import tempfile
from stratos_os.shell.deference import boot_stratos
from stratos_os.shell.saturator import IndustrialSaturator


@pytest.fixture
def env():
    root = "./.test_shell_assets"
    if os.path.exists(root):
        shutil.rmtree(root)

    from stratos_os.core.manifold import SovereignTorus
    from stratos_os.shell.deference import SovereignLoader

    torus = SovereignTorus(root_dir=root)
    loader = SovereignLoader(torus)
    sys.meta_path.insert(0, loader)

    yield torus, loader

    if loader in sys.meta_path:
        sys.meta_path.remove(loader)
    if os.path.exists(root):
        shutil.rmtree(root)

    to_del = [m for m in sys.modules if m.startswith('stratos')]
    for m in to_del:
        del sys.modules[m]


def test_saturator_and_loader(env):
    torus, loader = env
    saturator = IndustrialSaturator(torus)

    def my_func():
        return "hello from manifold"

    saturator.ingest_function("test.hello", my_func)

    import stratos.test.hello as hello_module
    assert hello_module.my_func() == "hello from manifold"


def test_saturator_ingest_module(env):
    torus, loader = env
    saturator = IndustrialSaturator(torus)

    # Create a dummy module file to ingest
    with tempfile.TemporaryDirectory() as tmpdir:
        sys.path.append(tmpdir)
        module_path = os.path.join(tmpdir, "dummy_mod.py")
        with open(module_path, "w") as f:
            f.write("""
def dummy_add(a, b):
    return a + b

def _private():
    pass
""")

        try:
            # Ingest the dummy module
            saturator.ingest_module("dummy_mod")

            # Check if function is accessible as a sub-module
            import stratos.dummy_mod.dummy_add as dummy_add_logic
            assert dummy_add_logic.dummy_add(10, 20) == 30

            # Verify private functions were NOT ingested
            # They should not be retrievable, which means confidence < T_safe
            v, sim = torus.retrieve("dummy_mod._private")
            assert v is None
            assert sim < torus.t_safe
        finally:
            if tmpdir in sys.path:
                sys.path.remove(tmpdir)
            if "dummy_mod" in sys.modules:
                del sys.modules["dummy_mod"]


if __name__ == "__main__":
    # If this test file is run directly, it will boot the torus and run the loader test
    # (Optional, but useful for quick verification)
    t = boot_stratos()
