import os
from stratos_os import boot_stratos, IndustrialSaturator

def populate():
    torus = boot_stratos()
    saturator = IndustrialSaturator(torus)

    # 1. FS Operations
    def list_dir(path='.'):
        import os
        return os.listdir(path)

    def read_file(path):
        with open(path, 'r') as f:
            return f.read()

    # 2. Math Utilities
    def add(a, b): return a + b
    def mul(a, b): return a * b

    # Ingest
    print("[POPULATE] Ingesting foundational logic...")
    saturator.ingest_function("fs.ls", list_dir)
    saturator.ingest_function("fs.read", read_file)
    saturator.ingest_function("math.add", add)
    saturator.ingest_function("math.mul", mul)

    print("[POPULATE] Manifold population complete.")

if __name__ == "__main__":
    populate()
