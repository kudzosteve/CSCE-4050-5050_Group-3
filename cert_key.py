from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json

with open("public.key",'rb') as f:
    server_pk = serialization.load_pem_public_key(f.read())

public_pem = server_pk.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

msg = f"This public key: {public_pem.hex()} belongs to 11507759"

msg_bytes = msg.encode('utf-8')

with open('secret_ca.key', 'rb') as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

signature = private_key.sign(
    msg_bytes,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

cert_data = {
    'message': msg,
    'signature': signature.hex()
}

with open("pk.cert", 'w') as f:
    json.dump(cert_data, f, indent=2)