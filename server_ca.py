from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from flask import Flask, jsonify, request
import hmac, hashlib
import json

app = Flask(__name__)

NONCE_SIZE = 12  # ChaCha20Poly1305 requires a 12-byte nonce
SESSION_KEY = None  # Variable to hold the session key

def load_private_key():
    with open('./secret.key', 'rb') as f:
        private_pem = f.read()
    return serialization.load_pem_private_key(private_pem, password=None)

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

def encrypt(data:bytes, nonce:bytes, key:bytes):
    cipher = ChaCha20Poly1305(key)
    return cipher.encrypt(nonce, data, None)

@app.route('/public_key', methods=['GET'])
def public_key():
    # Load the public key
    try:
        with open('./public.key', 'rb') as f:
            public_pem = f.read()
    except FileNotFoundError:
        return jsonify({'error': 'Server public key not found'}), 500
    # Reading the certificate
    with open("pk.cert", 'r') as f:
        cert = json.load(f)
    # Return the server's public key
    return jsonify({'pubkey': public_pem.decode('utf-8'), 'certificate': cert}), 200

@app.route('/session_key', methods=['POST'])
def session_key():
    global SESSION_KEY
    # Retrieve the data sent by the client
    body = request.get_json(silent=True)
    if not body or 'session_key' not in body:
        return jsonify({'error': 'Missing data in request'}), 400

    try:
        encrypted_data = bytes.fromhex(body['session_key'])
    except ValueError:
        return jsonify({'error': 'Encrypted data must be hex-encoded'}), 400

    # Try to decrypt the session key
    try:
        private_key = load_private_key()    # Get the non-serialized private key
        session_key = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        return jsonify({'error': 'Failed to decrypt session key'}), 400

    # If the key is not 32 bytes long, return an error
    if len(session_key) != 32:
        return jsonify({'error': 'Session key must be 32 bytes'}), 400

    # Now save the session key to the global variable and return a success message
    SESSION_KEY = session_key
    return jsonify({'status': 'OK'}), 200

@app.route('/weather', methods=['POST'])
def weather():
    body = request.get_json(silent=True)
    if not body or 'nonce' not in body:
        return jsonify({'error': 'Missing nonce in request body'}), 400

    try:
        nonce = bytes.fromhex(body['nonce'])
    except ValueError:
        return jsonify({'error': 'Nonce must be a hex-encoded string'}), 400

    if len(nonce) != NONCE_SIZE:
        return jsonify({'error': f'Nonce must be exactly {NONCE_SIZE} bytes ({NONCE_SIZE * 2} hex chars)'}), 400

    return weather_auth_enc(nonce)

def weather_auth_enc(nonce: bytes):
    global SESSION_KEY
    if SESSION_KEY is None:
        return jsonify({'error': 'Failed to establish a session'}), 403

    data = {
        'location': 'Denton, TX',
        'temperature_c': '10',
        'temperature_f': '50',
        'condition': 'Partly cloudy',
        'humidity': '27'
    }

    json_data = json.dumps(data).encode()       # Convert the data into a JSON string
    encryption_key, hmac_key = get_auth_keys(SESSION_KEY)   # Get the keys for authentication
    encrypted_data = encrypt(json_data, nonce, encryption_key)  # Encrypt the data

    # Create a HMAC signature of the encrypted data
    signature = hmac.new(hmac_key, encrypted_data, hashlib.sha256).hexdigest()

    # Construct the reply and return it (nonce is omitted — client already has it)
    reply = {
        'data': encrypted_data.hex(),
        'signature': signature
    }
    return jsonify(reply), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
