import numpy as np
import hashlib
import os

dim = 1024
v = np.random.standard_normal(dim).astype(np.float32)
v = v / np.linalg.norm(v)

hash1 = hashlib.md5(v.tobytes()).hexdigest()

np.save("test_v.npy", v)
v2 = np.load("test_v.npy")

hash2 = hashlib.md5(v2.tobytes()).hexdigest()

print(f"Hash 1: {hash1}")
print(f"Hash 2: {hash2}")
print(f"Equal: {hash1 == hash2}")

v_stack = np.vstack([v, v])
np.save("test_v_stack.npy", v_stack)
v_stack_load = np.load("test_v_stack.npy")
v3 = v_stack_load[0]

hash3 = hashlib.md5(v3.tobytes()).hexdigest()
print(f"Hash 3: {hash3}")
print(f"Equal: {hash1 == hash3}")

# Clean up
os.remove("test_v.npy")
os.remove("test_v_stack.npy")
