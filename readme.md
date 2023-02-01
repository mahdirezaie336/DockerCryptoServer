# Crypto Server Wrapper

This is a wrapper for the `Coinbase` API. It is a simple wrapper that allows you to get the current price of a cryptocurrency in USD. It runs in a docker container and is meant to be used as a microservice. It is written in `Python` and uses the `Flask` framework.

## Usage

To use this wrapper, you must first create a `Coinbase` account and get an API key. You can do this by following instructions [here](https://help.coinbase.com/en/exchange/managing-my-account/how-to-create-an-api-key). Once you have an API key, put it in docker-compose.yml in the following line:

```yaml
environment:
    - API_KEY=<YOUR API KEY>
```

Then, bring up the container with the following command:

```bash
docker-compose up
```

Once the container is up, you can make a request to the server with the following command:

```bash
curl http://localhost:5000/<CRYPTO SYMBOL>
```

For example, to get the price of Bitcoin, you would run the following command:

```bash
curl http://localhost:5000/BTC
```
