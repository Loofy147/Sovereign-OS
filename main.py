from shell.deference import boot_stratos

# 1. Mount the Torus
os_kernel = boot_stratos()

# 2. Ingest foundational logic (Run once)
os_kernel.ingest("sys.echo", "def ping(): return 'Signal established.'")

# 3. Native Python Deference
import stratos.sys.echo as echo
print(echo.ping())
