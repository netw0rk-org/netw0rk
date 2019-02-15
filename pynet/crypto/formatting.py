"""
Currently the system is being designed to take in utf-8 encoded bytes
and return utf-8 encoded bytesself.
~~~
Is it best to use UTF-8?
~~~
@YCRYPTX
"""
import re

def binary_string(str_array):
    output = ""
    for w in str_array:
        output += w
    return output.encode()

#takes in timestamp of any type and returns its non-decimal rounded
# byte  utf-8 string representation
def timestamp(t):
    if isinstance(t, str):
        if re.match("^\d+?\.\d+?$", t) is None:
            # not float, but is it integer?
            if re.match("^\d+?", t) is None:
                raise ValueError("failed to convert string timestamp into int")
            else:
                # is integer
                return t.encode()
        else:
            #is float
            t_float = float(t)
            t_int = int(t_float)
            t_str = str(t_int)
            return t_str.encode()
    elif isinstance(t, bytes):
        t_str = (t).decode("utf-8")
        if re.match("^\d+?\.\d+?$", t_str) is None:
            # not a float, but is it an integer ?
            if re.match("^\d+?", t_str) is None:
                raise ValueError("failed to convert bytes timestamp into int")
            else:
                return t
        else:
            t_float = float(t_str)
            t_int = int(t_float)
            t_str = str(t_int)
            return t_str.encode()
    elif isinstance(t, float):
        t_int = int(t)
        t_str = str(t_int)
        return t_str.encode()
    elif isinstance(t, int):
        t_str = str(t)
        return t_str.encode()
    else:
        raise ValueError("Failed to read timestamp")

def int_ts(ts):
    return int(ts)
