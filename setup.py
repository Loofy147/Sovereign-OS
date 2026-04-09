import os
from shell.loader import initialize
from shell.saturator import IndustrialSaturator

# Initialize the Sovereign OS
os_kernel = initialize()

# Example 1: Manual Ingestion
logic_source = """
def pulse():
    return "Sovereign signal active."
"""
os_kernel.ingest("core.signal", logic_source)

# Example 2: Industrial Saturation
saturator = IndustrialSaturator(os_kernel)
# We can't easily saturate a complex package in this environment without it being installed,
# but we can try a small standard one if possible, or just demonstrate the call.
# saturator.saturate_package("json")

# Test Deference
try:
    import sovereign.core.signal as signal
    print(signal.pulse())
except ImportError as e:
    print(f"Import Error: {e}")

print("Bootstrap Complete.")
