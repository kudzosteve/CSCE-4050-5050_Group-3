from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from flask import Flask, jsonify
import secrets
import json
import hmac, hashlib

app = Flask(__name__)


@app.route('/weather')
def weather():
    return weather_macd()


def weather_macd():
    data ={
        'location': 'Denton, TX',
        'temperature_c': '10',
        'temperature_f': '50',
        'condition': 'Partly cloudy',
        'humidity': '28'
    }

    # Convert the data into a JSON string, then to bytes
    json_data = json.dumps(data).encode()

    # Create a HMAC signature of the data

    # Construct the reply and return it
    reply = {
        'data': json_data.decode(),
        'signature': "0ec7550dcfdbafa041d98ab7c6b75ff551832f84dbc1af57e80b6ff7450c6115"
    }
    return jsonify(reply), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5051, debug=True)
