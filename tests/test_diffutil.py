from src.diffutil import unified_diff_str

def test_diff_contains_change():
    a = "hostname OLD\n"
    b = "hostname NEW\n"
    diff = unified_diff_str(a, b, 'before', 'after')
    assert "-hostname OLD" in diff and "+hostname NEW" in diff
