# Same program as keygen.py, only the ouputs are renamed according to ca convention required
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def gen_rsa_pair():
    # Generate the private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Serialize the key pair
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Write each generated key onto a file
    with open('./public_ca.key', 'wb') as pk:
        pk.write(public_pem)

    with open('./secret_ca.key', 'wb') as sk:
        sk.write(private_pem)

    print('RSA key pair has been generated.')


if __name__ == '__main__':
    gen_rsa_pair()