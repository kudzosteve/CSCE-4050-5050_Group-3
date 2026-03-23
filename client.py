from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import requests
import json
import hmac, hashlib

API_URL = 'http://127.0.0.1:5050'

KEY = 'b9347c10442a7e0665460a6f8e56450100b8c1a8b3370a9462738a7b5d870d21'
KEY_HMAC = '0ec7550dcfdbafa041d98ab7c6b75ff551832f84dbc1af57e80b6ff7450c6115'

def decrypt(data:bytes, nonce:bytes):
    cipher = ChaCha20Poly1305(bytes.fromhex(KEY))
    return cipher.decrypt(nonce, data, None)

def get_weather_decrypted():
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
    
def get_weather_macd():
    the_url = f'{API_URL}/weather'
    response = requests.get(url=the_url)
    if response.status_code == 200:
        # Fetch the data and the signature
        the_data = response.json()['data']
        the_signature = response.json()['signature']

        # Create a HMAC signature of the data and compare it to the signature from the server
        signature = hmac.new(bytes.fromhex(KEY), the_data.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(signature, the_signature):
            # If the signatures match, return the data as a dictionary
            data = json.loads(the_data)
            return data
        else:
            return 'Data integrity check failed'
    else:
        return 'Failed to get data'
    
def get_weather_auth_enc():
    the_url = f'{API_URL}/weather'
    response = requests.get(url=the_url)
    if response.status_code == 200:
        # Fetch the data and the nonce as bytes
        the_data = bytes.fromhex(response.json()['data'])
        the_nonce = bytes.fromhex(response.json()['nonce'])
        the_signature = bytes.fromhex(response.json()['signature'])


        # Decrypt the data and return it as a dictionary
        signature = hmac.new(bytes.fromhex(KEY_HMAC), the_data, hashlib.sha256).digest()
        if not hmac.compare_digest(signature, the_signature):
            return 'Data integrity check failed'
        decrypted_data = decrypt(the_data, the_nonce)
        data = json.loads(decrypted_data.decode())
        return data
    else:
        return 'Failed to get data'
def get_weather():
    # You can switch between the two methods by commenting/uncommenting the appropriate line
    # return get_weather_decrypted()
    return get_weather_auth_enc()

def main():
    print(get_weather())


if __name__ == '__main__':
    main()
