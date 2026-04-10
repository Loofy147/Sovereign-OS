import shutil
import os
from stratos_os import boot_stratos, IndustrialSaturator


def _fs_ops(saturator):
    def list_dir(path='.'):
        import os
        return os.listdir(path)

    def read_file(path):
        with open(path, 'r') as f:
            return f.read()

    saturator.ingest_function("fs.ls", list_dir)
    saturator.ingest_function("fs.read", read_file)


def _math_utils(saturator):
    def add(a, b):
        return a + b

    def mul(a, b):
        return a * b

    saturator.ingest_function("math.add", add)
    saturator.ingest_function("math.mul", mul)


def _string_utils(saturator):
    def to_upper(s):
        return s.upper()

    def to_lower(s):
        return s.lower()

    def join_list(lst, sep=' '):
        return sep.join(map(str, lst))

    saturator.ingest_function("str.upper", to_upper)
    saturator.ingest_function("str.lower", to_lower)
    saturator.ingest_function("str.join_list", join_list)


def _dt_utils(saturator):
    def get_now():
        import datetime
        return datetime.datetime.now().isoformat()

    def format_date(dt_str, fmt='%Y-%m-%d'):
        import datetime
        dt = datetime.datetime.fromisoformat(dt_str)
        return dt.strftime(fmt)

    saturator.ingest_function("dt.now", get_now)
    saturator.ingest_function("dt.format", format_date)


def _coll_helpers(saturator):
    def filter_list(func, lst):
        return list(filter(func, lst))

    def map_list(func, lst):
        return list(map(func, lst))

    saturator.ingest_function("coll.filter_list", filter_list)
    saturator.ingest_function("coll.map_list", map_list)


def populate():
    # Clean population
    asset_dir = './.stratos_assets'
    if os.path.exists(asset_dir):
        shutil.rmtree(asset_dir)

    torus = boot_stratos()
    saturator = IndustrialSaturator(torus)

    print("[POPULATE] Ingesting foundational logic...")
    _fs_ops(saturator)
    _math_utils(saturator)
    _string_utils(saturator)
    _dt_utils(saturator)
    _coll_helpers(saturator)

    print("[POPULATE] Manifold population complete.")


if __name__ == "__main__":
    populate()
