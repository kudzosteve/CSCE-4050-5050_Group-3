import requests

API_URL = 'http://127.0.0.1:5050'

def get_weather():
    the_url = f'{API_URL}/weather'
    response = requests.get(url=the_url)
    return response.json() if response.status_code == 200 else 'Failed to get data'

def main():
    print(get_weather())


if __name__ == '__main__':
    main()
