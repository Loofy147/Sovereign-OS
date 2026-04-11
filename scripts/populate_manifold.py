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


def _json_units(saturator):
    def loads(json_str):
        import json
        return json.loads(json_str)

    def dumps(obj):
        import json
        return json.dumps(obj)

    saturator.ingest_function("json.loads", loads)
    saturator.ingest_function("json.dumps", dumps)


def _net_units(saturator):
    def get(url):
        import urllib.request
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')

    def post(url, data_dict):
        import urllib.request
        import urllib.parse
        import json
        data = json.dumps(data_dict).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')

    saturator.ingest_function("net.get", get)
    saturator.ingest_function("net.post", post)


def _sys_units(saturator):
    def get_platform():
        import sys
        return sys.platform

    def get_version():
        import sys
        return sys.version

    def get_env(key, default=None):
        import os
        return os.environ.get(key, default)

    saturator.ingest_function("sys.get_platform", get_platform)
    saturator.ingest_function("sys.get_version", get_version)
    saturator.ingest_function("sys.get_env", get_env)


def _crypto_units(saturator):
    def sha256(text):
        import hashlib
        return hashlib.sha256(text.encode()).hexdigest()

    def b64encode(text):
        import base64
        return base64.b64encode(text.encode()).decode()

    def b64decode(encoded):
        import base64
        return base64.b64decode(encoded.encode()).decode()

    saturator.ingest_function("crypto.sha256", sha256)
    saturator.ingest_function("crypto.b64encode", b64encode)
    saturator.ingest_function("crypto.b64decode", b64decode)


def _util_units(saturator):
    def regex_match(pattern, text):
        import re
        return bool(re.match(pattern, text))

    def get_temp_dir():
        import tempfile
        return tempfile.gettempdir()

    saturator.ingest_function("utils.regex_match", regex_match)
    saturator.ingest_function("utils.get_temp_dir", get_temp_dir)


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
    _json_units(saturator)
    _net_units(saturator)
    _sys_units(saturator)
    _crypto_units(saturator)
    _util_units(saturator)

    print("[POPULATE] Manifold population complete.")


if __name__ == "__main__":
    populate()
