from context import formatting
import time
import re

def t_timestamp():
    #sanity
    t_float = time.time()
    t_int = int(t_float)
    t_str = str(t_float)
    t_bytes = bytes(t_str, "utf-8")
    assert isinstance(t_float, float), "failed to generate float timestamp"
    assert isinstance(t_int, int), "failed to convert float timestamp to int"
    assert isinstance(t_bytes, bytes), "failed to convert string timestamp to bytes"
    assert isinstance(t_str, str), "failed to convert float timestamp to string"

    expected_result = bytes(str(t_int),"utf-8")
    assert expected_result == formatting.timestamp(t_float), "failed formatting t_float"
    assert expected_result == formatting.timestamp(t_int), "failed formatting t_int"
    assert expected_result == formatting.timestamp(t_str), "failed formatting t_str"
    assert expected_result == formatting.timestamp(t_bytes), "failed formatting t_bytes"
    try:
        formatting.timestamp(b'this is bad')
        assert False, "failed to raise ValueError on bad (i.e. none int/float) bytes data"
    except:
        True
    try:
        formatting.timestamp("this is also bad")
        assert False, "failed to raise ValueError on bad (i.e. none int/float) string data"
    except:
        True



t_timestamp()
