import pytest
import json
import cbpro.auth
import cbpro.messenger
import cbpro.models
import cbpro.public


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
