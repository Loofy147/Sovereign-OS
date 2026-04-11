import os
import shutil
import pytest
from stratos_os.core.coordinator import TGICoordinator

@pytest.fixture
def coordinator():
    path = './.test_coordinator'
    if os.path.exists(path):
        shutil.rmtree(path)
    coord = TGICoordinator(root_dir=path)
    yield coord
    # shutil.rmtree(path)

def test_manifold_isolation(coordinator):
    # Ingest into base
    coordinator.base.ingest("math.add", "def add(a, b): return a + b")

    # Retrieve from base should succeed
    v_base, sim_base = coordinator.base.retrieve("math.add")
    assert v_base is not None

    # Retrieve from chain should fail (confidence below t_safe)
    v_chain, sim_chain = coordinator.chain.retrieve("math.add")
    assert v_chain is None
    assert sim_chain < coordinator.chain.t_safe

def test_routing(coordinator):
    coordinator.base.ingest("core_logic", "logic_v1")
    coordinator.proof.ingest("verified_logic", "logic_v2")

    manifold_name, v, sim = coordinator.route_query("core_logic")
    assert manifold_name == "base"

    manifold_name, v, sim = coordinator.route_query("verified_logic")
    assert manifold_name == "proof"

if __name__ == "__main__":
    pytest.main([__file__])
