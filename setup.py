import os
from deference import initialize

os_kernel = initialize()

# Example: Ingesting a sovereign networking tool
logic_source = """
def pulse():
    return "Sovereign signal active."
"""

os_kernel.ingest("core.signal", logic_source)

# Test Deference
import sovereign.core.signal as signal
print(signal.pulse())
