from itertools import islice
from dateutil.relativedelta import relativedelta
from tests.unit.utils import Teardown

import datetime
import pytest
import inspect

import cbpro.messenger
import cbpro.public


class TestPublicClient(object):
    def test_public_attr(self, public_client):
        assert hasattr(public_client, 'products')
        assert hasattr(public_client, 'currencies')
        assert hasattr(public_client, 'time')
        assert hasattr(public_client, 'history')

    def test_public_products(self, public_client):
        products = public_client.products
        assert isinstance(products, cbpro.messenger.Subscriber)
        assert isinstance(products, cbpro.public.Products)
        assert hasattr(products, 'list')
        assert hasattr(products, 'get')
        assert hasattr(products, 'order_book')
        assert hasattr(products, 'ticker')
        assert hasattr(products, 'trades')
        assert hasattr(products, 'history')
        assert hasattr(products, 'stats')

    def test_public_currencies(self, public_client):
        currencies = public_client.currencies
        assert isinstance(currencies, cbpro.messenger.Subscriber)
        assert isinstance(currencies, cbpro.public.Currencies)
        assert hasattr(currencies, 'list')
        assert hasattr(currencies, 'get')

    def test_public_time(self, public_client):
        time = public_client.time
        assert isinstance(time, cbpro.messenger.Subscriber)
        assert isinstance(time, cbpro.public.Time)
        assert hasattr(time, 'get')

    def test_public_history(self, public_client):
        history = public_client.history
        assert isinstance(history, cbpro.messenger.Subscriber)
        assert isinstance(history, cbpro.public.History)
        assert hasattr(history, 'candles')


class TestPublicProducts(Teardown):
    def test_list(self, public_client):
        response = public_client.products.list()
        assert isinstance(response, list)
        assert 'id' in response[0]

    def test_get(self, public_client):
        response = public_client.products.get('BTC-USD')
        assert isinstance(response, dict)
        assert 'id' in response
        assert response['id'] == 'BTC-USD'
        assert response['base_currency'] == 'BTC'
        assert response['quote_currency'] == 'USD'

    @pytest.mark.parametrize('level', [1, 2, 3, None])
    def test_order_book(self, public_client, public_model, level):
        params = public_model.products.order_book(level=level)
        response = public_client.products.order_book('BTC-USD', params=params)

        assert type(response) is dict
        assert 'sequence' in response
        assert 'asks' in response
        assert 'bids' in response

        if level in (1, None):
            asks = len(response['asks']) == 1
            bids = len(response['bids']) == 1
            assert asks or bids

        if level == 2:
            asks = len(response['asks']) <= 50
            bids = len(response['bids']) <= 50
            assert asks or bids

        if level == 3:
            asks = len(response['asks']) > 50
            bids = len(response['bids']) > 50
            assert asks or bids

    def test_ticker(self, public_client):
        response = public_client.products.ticker('BTC-USD')
        assert isinstance(response, dict)
        assert 'trade_id' in response
        assert 'price' in response
        assert 'size' in response

    def test_trades(self, public_client):
        response = public_client.products.trades('BTC-USD')
        assert inspect.isgenerator(response)
        response = list(islice(response, 200))
        assert 'trade_id' in response[0]

    current_time = datetime.datetime.now()

    @pytest.mark.parametrize('start,end,granularity',
                             [(current_time - relativedelta(months=1),
                               current_time, 21600)])
    def test_history(self,
                     public_client,
                     public_model,
                     start,
                     end,
                     granularity):

        params = public_model.products.history(start, end, granularity)
        response = public_client.products.history('BTC-USD', params=params)

        assert isinstance(response, list)

        for ticker in response:
            assert all([type(tick) in (int, float) for tick in ticker])

    def test_stats(self, public_client):
        response = public_client.products.stats('BTC-USD')
        assert isinstance(response, dict)
        assert 'volume_30day' in response


class TestPublicCurrencies(Teardown):
    def test_list(self, public_client):
        response = public_client.currencies.list()
        assert isinstance(response, list)
        assert 'name' in response[0]
        assert 'details' in response[0]

    def test_get(self, public_client):
        response = public_client.currencies.get('BTC')
        assert isinstance(response, dict)
        assert 'id' in response
        assert response['id'] == 'BTC'


class TestPublicTime(Teardown):
    def test_get(self, public_client):
        response = public_client.time.get()
        assert isinstance(response, dict)
        assert 'iso' in response


class TestPublicHistory(Teardown):
    @pytest.mark.parametrize('n_days', [1, 300, 301, 600, 601])
    def test_candles(self, public_client, n_days):
        """Test that we can get more than 300 candles despite the limit of 300 candles/request."""
        # arrange
        product_id = 'BTC-USD'
        granularity = 86400  # daily
        end = datetime.datetime.now()
        start = end - datetime.timedelta(seconds=granularity*n_days)
        params = {"start": start.isoformat(), "end": end.isoformat(), "granularity": granularity}

        # act
        response = public_client.history.candles(product_id, params)

        # assert
        assert isinstance(response, list)
        assert isinstance(response[0], list)
        assert len(response) == n_days
        assert len(response[0]) == 6

