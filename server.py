# Use Flast
import flask
import requests
import redis
import os
from datetime import timedelta

# Create the application.
APP = flask.Flask(__name__)

# Get environment variable. If not exist set to default
API_KEY = os.environ.get('API_KEY', 'demo')
PORT_NUMBER = int(os.environ.get('PORT_NUMBER', 5000))
MINUTES_TO_LIVE = int(os.environ.get('MINUTES_TO_LIVE', 5))
DEFAULT_CRYPTO = os.environ.get('DEFAULT_CRYPTO', 'BTC')
API_ADDRESS = os.environ.get('API_ADDRESS', 'https://rest.coinapi.io/v1/assets/')
REDIS_SERVER = os.environ.get('REDIS_SERVER', 'redis-server-service')

# Create redis object
r = redis.Redis(host=REDIS_SERVER, port=6379)


# A route to get the current price of input cryptocurrency
@APP.route('/<crypto>', methods=['GET'])
def api_all(crypto):
    # Check if is cached in redis and less than 5 minutes is passed
    if r.exists(crypto) and r.ttl(crypto) > 0:
        return {'name': crypto, 'price': r.get(crypto)}

    # Get data from the API
    response = requests.get(f'{API_ADDRESS}{crypto}', headers={'X-CoinAPI-Key': API_KEY})

    # Convert to JSON
    data = response.json()[0]
    price = data['price_usd']
    name = data['name']
    r.setex(crypto, timedelta(minutes=MINUTES_TO_LIVE), price)
    return {'name': name, 'price': price}


@APP.route('/', methods=['GET'])
def api_root():
    return api_all(DEFAULT_CRYPTO)


# Run the application.
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=PORT_NUMBER, debug=True)
