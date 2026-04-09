import pytest
import numpy as np
import os
import shutil
from stratos_os.core.manifold import SovereignTorus
from stratos_os.core.scan import scan_manifold_integrity


@pytest.fixture
def torus():
    root = "./.test_stratos_assets"
    if os.path.exists(root):
        shutil.rmtree(root)
    t = SovereignTorus(dim=1024, shard_cap=2, root_dir=root)
    yield t
    if os.path.exists(root):
        shutil.rmtree(root)


def test_vector_generation(torus):
    v1 = torus._generate_vec("test", salt="base:")
    v2 = torus._generate_vec("test", salt="base:")
    v3 = torus._generate_vec("test", salt="src:")

    assert np.allclose(v1, v2)
    assert not np.allclose(v1, v3)
    assert np.isclose(np.linalg.norm(v1), 1.0)


def test_ingest_and_retrieve(torus):
    identity = "test.logic"
    payload = "def test(): return True"
    torus.ingest(identity, payload)

    v_ret, sim = torus.retrieve(identity)
    assert v_ret is not None
    assert sim >= torus.t_safe


def test_shard_overflow(torus):
    # Shard cap is 2
    torus.ingest("id1", "val1")
    torus.ingest("id2", "val2")
    assert len(torus.shards) == 1

    torus.ingest("id3", "val3")
    assert len(torus.shards) == 2

    v, sim = torus.retrieve("id1")
    assert v is not None
    v, sim = torus.retrieve("id3")
    assert v is not None


def test_integrity_scan(torus):
    torus.ingest("id1", "val1")
    torus.ingest("id2", "val2")

    is_safe, max_sim = scan_manifold_integrity(torus)
    # With random vectors of D=1024, cross-similarity should be low
    assert is_safe
    assert max_sim < 0.094
