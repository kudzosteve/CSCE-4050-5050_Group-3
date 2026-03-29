from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import hmac, hashlib
import requests
import secrets
import json


API_URL = 'http://127.0.0.1:5050'
WEATHER_URL = f'{API_URL}/weather'
PUBLIC_KEY_URL = f'{API_URL}/public_key'
SESSION_KEY_URL = f'{API_URL}/session_key'

def get_server_public_key():
    response = requests.get(PUBLIC_KEY_URL)
    if response.status_code == 200:
        public_pem = response.json()['pubkey']
        return serialization.load_pem_public_key(public_pem.encode('utf-8'))
    else:
        return 'Failed to get public key'

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
    server_public_key = get_server_public_key() # Retrieve the server's public key
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
