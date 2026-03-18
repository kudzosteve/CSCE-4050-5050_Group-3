from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import requests
import json

API_URL = 'http://127.0.0.1:5050'

KEY = 'b9347c10442a7e0665460a6f8e56450100b8c1a8b3370a9462738a7b5d870d21'

def decrypt(data:bytes, nonce:bytes):
    cipher = ChaCha20Poly1305(bytes.fromhex(KEY))
    return cipher.decrypt(nonce, data, None)

def get_weather():
    the_url = f'{API_URL}/weather'
    response = requests.get(url=the_url)
    if response.status_code == 200:
        # Fetch the data and the nonce as bytes
        the_data = bytes(response.json()['data'])
        the_nonce = bytes(response.json()['nonce'])

        # Decrypt the data and return it as a dictionary
        decrypted_data = decrypt(the_data, the_nonce)
        data = json.loads(decrypted_data.decode())
        return data
    else:
        return 'Failed to get data'

def main():
    print(get_weather())


if __name__ == '__main__':
    main()
