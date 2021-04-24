# For public requests to the Coinbase exchange
# Copyright (c) 2017 Daniel Paquin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import cbpro.auth
import cbpro.messenger


class Public(object):
    def __init__(self,
                 url: str = None,
                 auth: cbpro.auth.Auth = None,
                 timeout: int = None) -> None:

        api = 'https://api.pro.coinbase.com'
        url = api if url is None else url.rstrip('/')
        timeout = 30 if timeout is None else timeout

        self.messenger = cbpro.messenger.Messenger(url, auth, timeout)

    def get_products(self) -> list:
        # source: https://docs.pro.coinbase.com/?python#products
        return self.messenger.get('/products')

    def get_product_order_book(self,
                               product_id: str,
                               level: int = None) -> dict:
        # Level 1 and Level 2 are recommended for polling. For the most
        # up-to-date data, consider using the websocket stream.
        #
        # **Caution**: Level 3 is only recommended for users wishing to
        # maintain a full real-time order book using the websocket
        # stream. Abuse of Level 3 via polling will cause your access to
        # be limited or blocked.
        #
        # source: https://docs.pro.coinbase.com/?python#get-single-product
        if level is None:
            level = 1

        params = {'level': level}

        return self.messenger.get(
            f'/products/{product_id}/book', params=params
        )

    def get_product_ticker(self, product_id: str) -> dict:
        # **Caution**: Polling is discouraged in favor of connecting via
        # the websocket stream and listening for match messages.
        #
        # source: https://docs.pro.coinbase.com/?python#get-product-ticker
        return self.messenger.get(f'/products/{product_id}/ticker')

    def get_product_trades(self, product_id: str) -> list:
        # source: https://docs.pro.coinbase.com/?python#get-trades
        return self.messenger.paginate(f'/products/{product_id}/trades')

    def get_product_historic_rates(self,
                                   product_id: str,
                                   start: str = None,
                                   end: str = None,
                                   granularity: int = None) -> list:
        # Rates are returned in grouped buckets based on requested
        # `granularity`. If start, end, and granularity aren't provided,
        # the exchange will assume some (currently unknown) default values.
        #
        # **Caution**: Historical rates should not be polled frequently.
        # If you need real-time information, use the trade and book
        # endpoints along with the websocket feed.
        #
        # source: https://docs.pro.coinbase.com/?python#get-historic-rates
        params = {}

        if start is not None:
            params['start'] = start

        if end is not None:
            params['end'] = end

        if granularity is not None:
            accepted = [60, 300, 900, 3600, 21600, 86400]

            if granularity not in accepted:
                raise ValueError(
                    f'Specified granularity is {granularity}, '
                    f'must be in approved values: {accepted}'
                )

            params['granularity'] = granularity

        return self.messenger.get(
            f'/products/{product_id}/candles', params=params
        )

    def get_product_24hr_stats(self, product_id: str) -> dict:
        # source: https://docs.pro.coinbase.com/?python#get-24hr-stats
        return self.messenger.get(f'/products/{product_id}/stats')

    def get_currencies(self) -> list:
        return self.messenger.get('/currencies')

    def get_time(self) -> dict:
        # Server time in ISO and epoch format (decimal seconds
        # since Unix epoch).
        return self.messenger.get('/time')
