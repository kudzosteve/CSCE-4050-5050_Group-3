from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from flask import Flask, jsonify
import secrets
import json
import hmac, hashlib

app = Flask(__name__)
KEY = 'b9347c10442a7e0665460a6f8e56450100b8c1a8b3370a9462738a7b5d870d21'
KEY_HMAC = '0ec7550dcfdbafa041d98ab7c6b75ff551832f84dbc1af57e80b6ff7450c6115'

def encrypt(data:bytes):
    cipher = ChaCha20Poly1305(bytes.fromhex(KEY))
    nonce = secrets.token_bytes(12)
    ciphertext = cipher.encrypt(nonce, data, None)
    return ciphertext, nonce

@app.route('/weather')
def weather():
    return weather_auth_enc()


def weather_encrypted():
    data ={
        'location': 'Denton, TX',
        'temperature_c': '10',
        'temperature_f': '50',
        'condition': 'Partly cloudy',
        'humidity': '27'
    }

    # Convert the data into a JSON string, then to bytes and encrypt it
    json_data = json.dumps(data).encode()
    encrypted_data, nonce = encrypt(json_data)

    # Construct the reply and return it
    reply = {
        'data': encrypted_data.hex(),
        'nonce': nonce.hex()
    }
    return jsonify(reply), 200


def weather_macd():
    data ={
        'location': 'Denton, TX',
        'temperature_c': '10',
        'temperature_f': '50',
        'condition': 'Partly cloudy',
        'humidity': '27'
    }

    # Convert the data into a JSON string, then to bytes
    json_data = json.dumps(data).encode()

    # Create a HMAC signature of the data
    signature = hmac.new(bytes.fromhex(KEY), json_data, hashlib.sha256).hexdigest()
    with open('tag.txt', 'w') as f:
        f.write(signature)
        
    # Construct the reply and return it
    reply = {
        'data': json_data.decode(),
        'signature': signature
    }
    return jsonify(reply), 200

def weather_auth_enc():
    data ={
        'location': 'Denton, TX',
        'temperature_c': '10',
        'temperature_f': '50',
        'condition': 'Partly cloudy',
        'humidity': '27'
    }

    # Convert the data into a JSON string, then to bytes and encrypt it
    json_data = json.dumps(data).encode()
    encrypted_data, nonce = encrypt(json_data)

    # Create a HMAC signature of the encrypted data
    signature = hmac.new(bytes.fromhex(KEY_HMAC), encrypted_data, hashlib.sha256).hexdigest()
    
    # Construct the reply and return it
    reply = {
        'data': encrypted_data.hex(),
        'nonce': nonce.hex(),
        'signature': signature
    }

    with open("responses.bin", 'wb') as f:
        f.write(encrypted_data)
        f.write(nonce)
        f.write(bytes.fromhex(signature))

    return jsonify(reply), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
