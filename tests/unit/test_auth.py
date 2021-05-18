import pytest
import requests
import cbpro.auth


def test_token(config):
    key, secret, passphrase = config

    token = cbpro.auth.Token(key, secret, passphrase)

    assert hasattr(token, 'key')
    assert hasattr(token, 'secret')
    assert hasattr(token, 'passphrase')

    assert isinstance(token.key, str)
    assert isinstance(token.secret, str)
    assert isinstance(token.passphrase, str)


def test_auth(config):
    key, secret, passphrase = config
    auth = cbpro.auth.Auth(key, secret, passphrase)

    assert hasattr(auth, 'token')
    assert isinstance(auth.token, cbpro.auth.Token)
    assert callable(auth)


@pytest.mark.skip
def test_auth_request(sandbox, auth):
    assert 'sandbox' in sandbox

    url = sandbox + '/accounts'
    params = None

    response = requests.get(
        url,
        params=params,
        auth=auth,
        timeout=30
    )

    print(response.json())

    assert response.status_code == 200
