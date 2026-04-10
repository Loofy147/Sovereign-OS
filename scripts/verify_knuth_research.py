import sys
import os

# Add src to path for direct imports
sys.path.insert(0, os.path.abspath('src'))

from stratos_os.shell.deference import boot_stratos
from stratos_os.shell.saturator import IndustrialSaturator

def run_research_verification():
    print("--- [TGI RESEARCH VERIFICATION] ---")

    # 1. Boot the Sovereign Manifold
    torus = boot_stratos()

    # 2. Manually ingest the whole module source to allow inter-function dependencies
    print("[STEP 1] Ingesting Knuth's Research Module into the Manifold...")
    module_path = "src/stratos_os/research/knuth_cycles.py"
    with open(module_path, "r") as f:
        source = f.read()

    # We ingest it with the identity that we will use to import it
    torus.ingest("stratos_os.research.knuth_cycles", source)
    print(f"[SATURATOR] Anchored module: stratos_os.research.knuth_cycles")

    # 3. Native Python Deference via SovereignLoader
    print("[STEP 2] Deferring execution to the Holographic Substrate...")

    try:
        # This import is intercepted by SovereignLoader
        import stratos.stratos_os.research.knuth_cycles as research

        # 4. Execute and Verify Proven Results
        # verify_hamiltonian will now find get_arc_target in its global scope (the module dict)
        for m in [3, 5, 7]:
            success, msg = research.verify_hamiltonian(m)
            status = "PROVEN" if success else "FAILED"
            print(f"[RESULT] m={m}: {status} - {msg}")

    except ImportError as e:
        print(f"[CRITICAL] Loader failed to resolve research logic: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Verification execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("--- [VERIFICATION COMPLETE] ---")

if __name__ == "__main__":
    run_research_verification()
