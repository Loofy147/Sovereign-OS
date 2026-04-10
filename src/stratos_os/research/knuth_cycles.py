def get_arc_target(m, i, j, k, cycle_idx):
    """
    Python implementation of Knuth's (2026) Claude-like decomposition.
    Decomposes 3m^3 arcs of the discrete 3-torus into 3 Hamiltonian cycles.
    """
    s = (i + j + k) % m

    # The concrete three-boundary-case rule from Knuth (2026)
    if s == 0:
        d = "012" if j == m - 1 else "210"
    elif s == m - 1:
        d = "210" if i == 0 else "120"
    else:
        d = "201" if i == m - 1 else "102"

    gen = d[cycle_idx]

    if gen == '0':
        return (i + 1) % m, j, k
    elif gen == '1':
        return i, (j + 1) % m, k
    elif gen == '2':
        return i, j, (k + 1) % m
    return i, j, k

def verify_hamiltonian(m):
    """
    Verifies that the construction yields 3 Hamiltonian cycles for a given m.
    """
    if m % 2 == 0:
        return False, "Construction only proven for odd m."

    total_vertices = m**3

    for c in range(3):
        visited = set()
        curr = (0, 0, 0)

        for _ in range(total_vertices):
            if curr in visited:
                return False, f"Cycle {c} closed prematurely at {curr} after {len(visited)} steps."
            visited.add(curr)
            curr = get_arc_target(m, curr[0], curr[1], curr[2], c)

        if curr != (0, 0, 0):
            return False, f"Cycle {c} failed to return to start."
        if len(visited) != total_vertices:
            return False, f"Cycle {c} only visited {len(visited)} vertices."

    return True, f"Verified: 3 Hamiltonian cycles of length {total_vertices} for m={m}."

if __name__ == "__main__":
    for m in [3, 5]:
        success, msg = verify_hamiltonian(m)
        print(f"m={m}: {msg}")
