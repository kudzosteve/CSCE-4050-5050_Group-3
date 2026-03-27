from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import requests
import secrets
import json
import hmac, hashlib

API_URL = 'http://127.0.0.1:5050'

KEY = 'b9347c10442a7e0665460a6f8e56450100b8c1a8b3370a9462738a7b5d870d21'
KEY_HMAC = '0ec7550dcfdbafa041d98ab7c6b75ff551832f84dbc1af57e80b6ff7450c6115'

def decrypt(data: bytes, nonce: bytes):
    cipher = ChaCha20Poly1305(bytes.fromhex(KEY))
    return cipher.decrypt(nonce, data, None)

def get_weather_auth_enc():
    the_url = f'{API_URL}/weather'

    # Generate a fresh nonce client-side and send it to the server
    nonce = secrets.token_bytes(12)
    response = requests.post(url=the_url, json={'nonce': nonce.hex()})

    if response.status_code == 200:
        the_data = bytes.fromhex(response.json()['data'])
        the_signature = bytes.fromhex(response.json()['signature'])

        # Verify HMAC before decrypting
        expected_sig = hmac.new(bytes.fromhex(KEY_HMAC), the_data, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_sig, the_signature):
            return 'Data integrity check failed'

        # Decrypt using the nonce we generated
        decrypted_data = decrypt(the_data, nonce)
        return json.loads(decrypted_data.decode())
    else:
        return f'Request failed ({response.status_code}): {response.text}'

def get_weather():
    return get_weather_auth_enc()

def main():
    print(get_weather())

if __name__ == '__main__':
    main()
