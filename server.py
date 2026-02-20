from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/weather')
def weather():
    data ={
        'location': 'Denton, TX',
        'temperature_c': '10',
        'temperature_f': '50',
        'condition': 'Partly cloudy',
        'humidity': '27'
    }
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050)