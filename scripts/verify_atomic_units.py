from stratos_os import boot_stratos

def verify():
    boot_stratos()

    print("--- [VERIFYING ATOMIC UNITS] ---")

    # Test JSON
    import stratos.json.loads as json_loads
    import stratos.json.dumps as json_dumps
    data = {"key": "value", "nested": [1, 2, 3]}
    j_str = json_dumps.dumps(data)
    j_obj = json_loads.loads(j_str)
    assert j_obj == data
    print("[OK] stratos.json verified.")

    # Test SYS
    import stratos.sys.get_platform as get_platform
    import stratos.sys.get_version as get_version
    platform = get_platform.get_platform()
    version = get_version.get_version()
    assert isinstance(platform, str)
    assert isinstance(version, str)
    print(f"[OK] stratos.sys verified (Platform: {platform}).")

    # Test CRYPTO
    import stratos.crypto.sha256 as sha256
    import stratos.crypto.b64encode as b64encode
    text = "stratos-os"
    hashed = sha256.sha256(text)
    encoded = b64encode.b64encode(text)
    assert len(hashed) == 64
    assert encoded == "c3RyYXRvcy1vcw=="
    print("[OK] stratos.crypto verified.")

    # Test UTILS
    import stratos.utils.regex_match as regex
    assert regex.regex_match(r"^stratos", "stratos-v7")
    assert not regex.regex_match(r"^stratos", "os-v7")
    print("[OK] stratos.utils verified.")

    # Test NET (Mock or local check if possible)
    import stratos.net.get as net_get
    import stratos.net.post as net_post
    assert hasattr(net_get, "get")
    assert hasattr(net_post, "post")
    print("[OK] stratos.net verified (Structure only).")

    print("--- [VERIFICATION COMPLETE] ---")

if __name__ == "__main__":
    verify()
