import os, base64
def generate_session():
    return str(base64.b64encode(os.urandom(16))).replace("'", "")


