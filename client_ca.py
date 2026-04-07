from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import hmac, hashlib
import requests
import secrets
import json
import re


API_URL = 'http://127.0.0.1:5050'
WEATHER_URL = f'{API_URL}/weather'
PUBLIC_KEY_URL = f'{API_URL}/public_key'
SESSION_KEY_URL = f'{API_URL}/session_key'

def get_server_public_key():
    response = requests.get(PUBLIC_KEY_URL)
    if response.status_code == 200:
        public_pem = response.json()['pubkey']
        certificate = response.json()['certificate']
        return serialization.load_pem_public_key(public_pem.encode('utf-8')), certificate
    else:
        return 'Failed to get public key'

# Function to check whether the server's pk is valid based on CA certificate
def verify_server_public_key(pk_hexstr, cert):
    signature = bytes.fromhex(cert['signature'])
    msg_str = cert['message']
    match = re.search("This public key: (.+) belongs to *", msg_str)
    msg = msg_str.encode('utf-8')
    server_pkstr = match.group(1)
    # First checking if public key in cert same as public key of server
    if pk_hexstr != server_pkstr:
        print("Public keys don't match")
        return False
    # Verifying cert signature
    with open("public_ca.key", 'rb') as f:
        ca_pub = serialization.load_pem_public_key(f.read())
    try:
        ca_pub.verify(
            signature,
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False


def get_auth_keys(session_key):
    # If the session key is a string,convert to bytes
    if isinstance(session_key, str):
        try:
            session_key = bytes.fromhex(session_key)
        except ValueError:
            session_key = session_key.encode('utf-8')

    # Create an encryption key and a hmac key from the session key
    encryption_key = hashlib.sha256(bytes(session_key) + b'key').digest()
    hmac_key = hashlib.sha256(bytes(session_key )+ b'mac').digest()
    return encryption_key, hmac_key

def exchange_session_key():
    server_public_key, cert = get_server_public_key() # Retrieve the server's public key
    # Verify the public key with the CA cert
    pk_bytes = server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    verified = verify_server_public_key(pk_bytes.hex(), cert)

    if not verified:
        print("Invalid certificate")
        exit()
    session_key = secrets.token_bytes(32)   # Generate a random 32-byte session key
    # Encrypt the session key
    encrypted_key = server_public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Send the encrypted session key to the server
    response = requests.post(SESSION_KEY_URL, json={'session_key': encrypted_key.hex()})
    if response.status_code != 200:
        return 'Failed to send session key to server'

    return session_key

def decrypt(data:bytes, nonce:bytes, session_key:bytes):
    # Get the key for the decryption
    the_key, _ = get_auth_keys(session_key)
    cipher = ChaCha20Poly1305(the_key)
    return cipher.decrypt(nonce, data, None)

def get_weather_auth_enc():
    # Generate a fresh nonce client-side and send it to the server
    nonce = secrets.token_bytes(12)
    session_key = exchange_session_key()  # Send the session key to the server
    response = requests.post(url=WEATHER_URL, json={'nonce': nonce.hex()})

    if response.status_code == 200:
        the_data = bytes.fromhex(response.json()['data'])
        the_signature = bytes.fromhex(response.json()['signature'])

        # Verify HMAC before decrypting
        _, hmac_key = get_auth_keys(session_key)
        expected_sig = hmac.new(hmac_key, the_data, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_sig, the_signature):
            return 'Data integrity check failed'

        # Decrypt the data with the generated nonce
        decrypted_data = decrypt(the_data, nonce, session_key)
        return json.loads(decrypted_data.decode())
    else:
        return f'Request failed ({response.status_code}): {response.text}'

def get_weather():
    return get_weather_auth_enc()

def main():
    print(get_weather())


if __name__ == '__main__':
    main()
