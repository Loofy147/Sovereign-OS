import pytest
import numpy as np
import os
import shutil
from stratos_os.core.manifold import SovereignTorus
from stratos_os.core.runtime import ChainRuntime


@pytest.fixture
def runtime():
    root = "./.test_runtime_assets"
    if os.path.exists(root):
        shutil.rmtree(root)
    t = SovereignTorus(dim=1024, root_dir=root)
    r = ChainRuntime(t)
    yield r
    if os.path.exists(root):
        shutil.rmtree(root)


def test_bind_frac(runtime):
    a = runtime.torus._generate_vec("a")
    b = runtime.torus._generate_vec("b")
    c = runtime.bind_frac(a, b)

    assert c.shape == (1024,)
    assert not np.allclose(c, a)
    assert not np.allclose(c, b)


def test_execute_chain(runtime):
    # Note: execute_chain uses torus._generate_vec to initialize and evolve state
    # but it doesn't necessarily need the IDs to be ingested into the torus first
    # because it just generates the vectors from the IDs.

    sequence = ["step1", "step2", "step3"]
    result = runtime.execute_chain(sequence)

    assert result.shape == (1024,)

    # Check cache
    chain_label = "->".join(sequence)
    assert chain_label in runtime.cache
    assert np.allclose(runtime.cache[chain_label], result)

    # Check persistence
    new_runtime = ChainRuntime(runtime.torus)
    assert chain_label in new_runtime.cache
    assert np.allclose(new_runtime.cache[chain_label], result)
