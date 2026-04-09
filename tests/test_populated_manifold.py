import pytest
import sys
from stratos_os.shell.deference import boot_stratos

@pytest.fixture(scope="module")
def torus():
    # boot_stratos will use .stratos_assets by default
    t = boot_stratos()
    yield t

def test_string_utilities(torus):
    import stratos.str.upper as upper
    import stratos.str.lower as lower
    import stratos.str.join_list as join_list

    assert upper.to_upper("hello") == "HELLO"
    assert lower.to_lower("WORLD") == "world"
    assert join_list.join_list([1, 2, 3], sep="-") == "1-2-3"

def test_datetime_utilities(torus):
    import stratos.dt.now as now
    import stratos.dt.format as fmt

    current = now.get_now()
    assert isinstance(current, str)
    formatted = fmt.format_date(current, "%Y")
    import datetime
    assert formatted == str(datetime.datetime.now().year)

def test_collection_helpers(torus):
    import stratos.coll.filter_list as filter_list
    import stratos.coll.map_list as map_list

    lst = [1, 2, 3, 4]
    evens = filter_list.filter_list(lambda x: x % 2 == 0, lst)
    assert evens == [2, 4]

    squared = map_list.map_list(lambda x: x * x, lst)
    assert squared == [1, 4, 9, 16]
