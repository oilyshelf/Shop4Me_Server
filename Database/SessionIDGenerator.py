import os, base64
def generate_session():
    return base64.b64encode(os.urandom(16))


for i in range(5):
    print(type(generate_session()))