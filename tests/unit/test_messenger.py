from tests.unit.utils import Teardown

import pytest
import requests
import inspect
import cbpro.messenger


class TestMessenger(Teardown):
    def test_messenger_attr(self, messenger):
        assert hasattr(messenger, 'auth')
        assert hasattr(messenger, 'url')
        assert hasattr(messenger, 'timeout')
        assert hasattr(messenger, 'session')
        assert hasattr(messenger, 'route')
        assert hasattr(messenger, 'get')
        assert hasattr(messenger, 'post')
        assert hasattr(messenger, 'delete')
        assert hasattr(messenger, 'paginate')

    def test_messenger_instance(self, messenger):
        assert isinstance(messenger.url, str)
        assert isinstance(messenger.timeout, int)
        assert isinstance(messenger.session, requests.Session)

    def test_messenger_get(self, messenger):
        response = messenger.get('/time')
        assert isinstance(response, (list, dict))

    @pytest.mark.skip
    def test_messenger_post(self, auth_messenger, private_model):
        order = private_model.orders.market('buy', 'BTC-USD', funds=10.0)
        response = auth_messenger.post('/orders', json=order)

        for key, value in response.items():
            print(f'{key}: {value}')

        assert isinstance(response, dict)

        assert 'message' not in response
        assert 'side' in response
        assert 'product_id' in response

        assert response['side'] == 'buy'
        assert response['product_id'] == 'BTC-USD'

    def test_messenger_paginate(self, messenger):
        response = messenger.paginate('/products/BTC-USD/trades')
        assert inspect.isgenerator(response)


class DummySubscriber(cbpro.messenger.Subscriber):
    pass


def test_subscriber(messenger):
    dummy = DummySubscriber(messenger)
    assert hasattr(dummy, 'messenger')
    assert isinstance(dummy.messenger, cbpro.messenger.Messenger)
