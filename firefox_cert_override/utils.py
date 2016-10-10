def b64pad(data):
    """
    Pad base64 data with '=' so that it's length is a multiple of 4.
    """
    missing = len(data) % 4
    if missing:
        data += b'=' * (4 - missing)
    return data
