def int_from_bytes(raw_bytes, start, end):
    """Shortcut for int.from_bytes with byteorder='little'"""
    return int.from_bytes(raw_bytes[start:end], byteorder='little')
