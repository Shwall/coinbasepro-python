import pytest
import json

import cbpro.auth
import cbpro.messenger
import cbpro.models
import cbpro.public
import cbpro.private


@pytest.fixture(scope='module')
def sandbox():
    return 'https://api-public.sandbox.pro.coinbase.com'


@pytest.fixture(scope='module')
def config():
    user = dict()
    with open('tests/auth.json.example', 'r') as file:
        user = json.load(file)
    return user['key'], user['secret'], user['passphrase']


@pytest.fixture(scope='module')
def auth(config):
    return cbpro.auth.Auth(*config)


@pytest.fixture(scope='module')
def messenger(sandbox):
    return cbpro.messenger.Messenger(url=sandbox)


@pytest.fixture(scope='module')
def auth_messenger(auth, sandbox):
    return cbpro.messenger.Messenger(auth=auth, url=sandbox)


@pytest.fixture(scope='module')
def public_model():
    return cbpro.models.PublicModel()


@pytest.fixture(scope='module')
def private_model():
    return cbpro.models.PrivateModel()


@pytest.fixture(scope='module')
def public_client(messenger):
    return cbpro.public.PublicClient(messenger)


@pytest.fixture(scope='module')
def private_client(auth_messenger):
    return cbpro.private.PrivateClient(auth_messenger)


@pytest.fixture(scope='module')
def account_id(private_client):
    accounts = private_client.accounts.list()
    account_usd = [a for a in accounts if a['currency'] == 'USD']
    return account_usd[0]['id']
