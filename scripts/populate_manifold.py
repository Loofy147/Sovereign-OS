import os
import datetime
from stratos_os import boot_stratos, IndustrialSaturator

def populate():
    torus = boot_stratos()
    saturator = IndustrialSaturator(torus)

    # --- 1. FS Operations ---
    def list_dir(path='.'):
        import os
        return os.listdir(path)

    def read_file(path):
        with open(path, 'r') as f:
            return f.read()

    # --- 2. Math Utilities ---
    def add(a, b): return a + b
    def mul(a, b): return a * b

    # --- 3. String Utilities ---
    def to_upper(s):
        return s.upper()

    def to_lower(s):
        return s.lower()

    def join_list(lst, sep=' '):
        return sep.join(map(str, lst))

    # --- 4. Datetime Utilities ---
    def get_now():
        import datetime
        return datetime.datetime.now().isoformat()

    def format_date(dt_str, fmt='%Y-%m-%d'):
        import datetime
        dt = datetime.datetime.fromisoformat(dt_str)
        return dt.strftime(fmt)

    # --- 5. Collection Helpers ---
    def filter_list(func, lst):
        return list(filter(func, lst))

    def map_list(func, lst):
        return list(map(func, lst))

    # Ingest
    print("[POPULATE] Ingesting foundational logic...")
    saturator.ingest_function("fs.ls", list_dir)
    saturator.ingest_function("fs.read", read_file)
    saturator.ingest_function("math.add", add)
    saturator.ingest_function("math.mul", mul)

    saturator.ingest_function("str.upper", to_upper)
    saturator.ingest_function("str.lower", to_lower)
    saturator.ingest_function("str.join_list", join_list)

    saturator.ingest_function("dt.now", get_now)
    saturator.ingest_function("dt.format", format_date)

    saturator.ingest_function("coll.filter_list", filter_list)
    saturator.ingest_function("coll.map_list", map_list)

    print("[POPULATE] Manifold population complete.")

if __name__ == "__main__":
    populate()
