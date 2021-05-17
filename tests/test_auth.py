import json
import requests

import cbpro.auth


def get_auth_config():
    config = dict()

    with open('tests/auth.json', 'r') as file:
        config = json.load(file)

    return config['key'], config['secret'], config['passphrase']


def test_token():
    key, secret, passphrase = get_auth_config()

    token = cbpro.auth.Token(key, secret, passphrase)

    assert hasattr(token, 'key')
    assert hasattr(token, 'secret')
    assert hasattr(token, 'passphrase')

    assert isinstance(token.key, str)
    assert isinstance(token.secret, str)
    assert isinstance(token.passphrase, str)


def test_auth():
    sandbox = 'https://api-public.sandbox.pro.coinbase.com'
    endpoint = '/accounts'
    url = sandbox + endpoint
    params = None

    assert 'sandbox' in url

    key, secret, passphrase = get_auth_config()
    auth = cbpro.auth.Auth(key, secret, passphrase)

    assert hasattr(auth, 'token')
    assert isinstance(auth.token, cbpro.auth.Token)

    response = requests.get(
        url,
        params=params,
        auth=auth,
        timeout=30
    )

    print(response.json())

    assert response.status_code == 200
