import numpy as np
import pytest
import shutil
import os
from stratos_os.core.manifold import SovereignTorus

@pytest.fixture
def torus():
    path = './.test_hierarchical'
    if os.path.exists(path):
        shutil.rmtree(path)
    # Shard cap = 2 to force many shards
    t = SovereignTorus(dim=512, shard_cap=2, root_dir=path)
    yield t

def test_hierarchical_retrieval(torus):
    # Ingest 10 items -> 5 shards
    items = [f"item_{i}" for i in range(10)]
    for item in items:
        torus.ingest(item, f"payload_{item}")

    assert len(torus.shards) == 5
    assert torus._shard_centroids.shape[0] == 5

    # Verify retrieval still works for all items
    for item in items:
        v, sim = torus.retrieve(item)
        assert v is not None
        assert sim > torus.t_safe

    # Verify retrieval for non-existent item fails
    v, sim = torus.retrieve("ghost_item")
    assert v is None
    assert sim < torus.t_safe

if __name__ == "__main__":
    pytest.main([__file__])
