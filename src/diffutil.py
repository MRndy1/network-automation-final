import difflib

def unified_diff_str(before, after, fromfile='before', tofile='after'):
    a = before.splitlines(True); b = after.splitlines(True)
    return ''.join(difflib.unified_diff(a, b, fromfile, tofile))
