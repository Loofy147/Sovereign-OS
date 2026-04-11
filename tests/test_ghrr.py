import numpy as np
from stratos_os.core.manifold import SovereignTorus

def test_bind_ghrr():
    torus = SovereignTorus(dim=1024)
    a = torus._generate_vec("A", salt="test:a")
    b = torus._generate_vec("B", salt="test:b")

    # GHRR bind
    c_ab = torus.bind_ghrr(a, b)
    c_ba = torus.bind_ghrr(b, a)

    # If it were commutative, c_ab == c_ba
    diff = np.linalg.norm(c_ab - c_ba)
    print(f"Norm diff between bind_ghrr(a, b) and bind_ghrr(b, a): {diff}")

    # We expect them to be different
    assert diff > 0.1, "GHRR should be non-commutative"

def test_ghrr_recovery():
    torus = SovereignTorus(dim=1024)
    a = torus._generate_vec("A", salt="test:a")
    b = torus._generate_vec("B", salt="test:b")

    c = torus.bind_ghrr(a, b)

    # Recovering with unbind_ghrr(c, a) should give b
    b_recovered = torus.unbind_ghrr(c, a)
    sim_b = np.dot(b_recovered, b)
    print(f"Sim with b: {sim_b}")
    assert sim_b > 0.7

def test_ghrr_sequence():
    """GHRR allows storing ordered sequences: (A, B) != (B, A)"""
    torus = SovereignTorus(dim=1024)
    a = torus._generate_vec("A")
    b = torus._generate_vec("B")

    seq1 = torus.bind_ghrr(a, b) # A followed by B
    seq2 = torus.bind_ghrr(b, a) # B followed by A

    sim = np.dot(seq1, seq2)
    assert sim < 0.1, f"Sequences should be distinct, sim: {sim}"

if __name__ == "__main__":
    test_bind_ghrr()
    test_ghrr_recovery()
    test_ghrr_sequence()
