import base64
def encode(to_encode):
    return str(base64.b64encode(to_encode.encode("ascii")).decode())
def decode(to_decode):
    return base64.b64decode(to_decode).decode("ascii")
