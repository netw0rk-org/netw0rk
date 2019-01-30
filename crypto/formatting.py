
def binary_string(string_array):
    output = b""
    for i in string_array:
        output += b"{}".format(i)
    return output
