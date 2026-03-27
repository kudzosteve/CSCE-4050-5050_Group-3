from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from flask import Flask, jsonify, request
import json
import hmac, hashlib

app = Flask(__name__)
KEY = 'b9347c10442a7e0665460a6f8e56450100b8c1a8b3370a9462738a7b5d870d21'
KEY_HMAC = '0ec7550dcfdbafa041d98ab7c6b75ff551832f84dbc1af57e80b6ff7450c6115'

NONCE_SIZE = 12  # ChaCha20Poly1305 requires a 12-byte nonce

def encrypt(data: bytes, nonce: bytes):
    cipher = ChaCha20Poly1305(bytes.fromhex(KEY))
    ciphertext = cipher.encrypt(nonce, data, None)
    return ciphertext

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
    data = {
        'location': 'Denton, TX',
        'temperature_c': '10',
        'temperature_f': '50',
        'condition': 'Partly cloudy',
        'humidity': '27'
    }

    # Convert the data into a JSON string, then to bytes and encrypt it
    json_data = json.dumps(data).encode()
    encrypted_data = encrypt(json_data, nonce)

    # Create a HMAC signature of the encrypted data
    signature = hmac.new(bytes.fromhex(KEY_HMAC), encrypted_data, hashlib.sha256).hexdigest()

    # Construct the reply and return it (nonce is omitted — client already has it)
    reply = {
        'data': encrypted_data.hex(),
        'signature': signature
    }

    with open("responses.bin", 'wb') as f:
        f.write(encrypted_data)
        f.write(bytes.fromhex(signature))

    return jsonify(reply), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
