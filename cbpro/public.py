import cbpro.messenger


class Products(cbpro.messenger.Subscriber):
    def list(self) -> list:
        return self.messenger.get('/products')

    def get(self, product_id: str) -> dict:
        return self.messenger.get(f'/products/{product_id}')

    def order_book(self, product_id: str, params: dict = None) -> dict:
        # NOTE:
        #   - This request is not paginated
        #   - Polling is discouraged for this method
        #   - Use the websocket stream for polling instead
        # https://docs.pro.coinbase.com/#get-product-order-book
        endpoint = f'/products/{product_id}/book'
        return self.messenger.get(endpoint, params=params)

    def ticker(self, product_id: str) -> dict:
        # NOTE:
        #   - Polling is discouraged for this method
        #   - Use the websocket stream for polling instead
        return self.messenger.get(f'/products/{product_id}/ticker')

    def trades(self, product_id: str, params: dict = None) -> list:
        return self.messenger.paginate(f'/products/{product_id}/trades', params=params)

    def history(self, product_id: str, params: dict = None) -> list:
        # NOTE:
        #   - Polling is discouraged for this method
        #   - Use the websocket stream for polling instead
        endpoint = f'/products/{product_id}/candles'
        return self.messenger.get(endpoint, params=params)

    def stats(self, product_id: str) -> dict:
        return self.messenger.get(f'/products/{product_id}/stats')


class Currencies(cbpro.messenger.Subscriber):
    def list(self) -> list:
        # NOTE: Not all currencies may be currently in use for trading
        return self.messenger.get('/currencies')

    def get(self, currency_id: str) -> dict:
        # NOTE: Currencies which have or had no representation in ISO 4217
        # may use a custom code
        return self.messenger.get(f'/currencies/{currency_id}')


class Time(cbpro.messenger.Subscriber):
    def get(self) -> dict:
        # NOTE: This endpoint does not require authentication
        # NOTE: The epoch field represents decimal seconds since Unix Epoch
        return self.messenger.get('/time')


class PublicClient(object):
    def __init__(self, messenger: cbpro.messenger.Messenger) -> None:
        self.products = Products(messenger)
        self.currencies = Currencies(messenger)
        self.time = Time(messenger)


def public_client(url=None):
    messenger = cbpro.messenger.Messenger(url=url)
    return PublicClient(messenger)
