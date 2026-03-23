from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from flask import Flask, jsonify
import secrets
import json
import hmac, hashlib

app = Flask(__name__)


@app.route('/weather')
def weather():
    return weather_fake()


def weather_fake():
    with open('responses.bin', 'rb') as f:
        data = f.read()
        signature = data[-32:]
        nonce = data[-44:-32]          # 12 bytes before the signature
        encrypted_data = data[:-44]  
        
    reply = {
        'data': encrypted_data.hex(),
        'nonce': nonce.hex(),
        'signature': signature.hex()
    }
    return jsonify(reply), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
