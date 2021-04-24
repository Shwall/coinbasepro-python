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
import requests
import cbpro.auth


class Messenger(object):
    def __init__(self,
                 url: str = None,
                 auth: cbpro.auth.Auth = None,
                 timeout: int = None) -> None:

        self.url = url
        self.auth = auth
        self.timeout = timeout

        self.session = requests.Session()

    def route(self, endpoint: str) -> str:
        return f'{self.url}{endpoint}'

    def get(self, endpoint: str, params: dict = None) -> list:
        url = self.route(endpoint)
        return self.session.get(
            url,
            params=None,
            auth=self.auth,
            timeout=self.timeout
        ).json()

    def post(self,
             endpoint: str,
             params: dict = None,
             json: dict = None) -> list:

        url = self.route(endpoint)
        return self.session.post(
            url,
            params=params,
            json=json,
            auth=self.auth,
            timeout=self.timeout
        ).json()

    def request(self, method: str,
                endpoint: str,
                params: dict = None,
                json: dict = None) -> list:

        url = self.route(endpoint)
        return self.session.request(
            method,
            url,
            json=json,
            params=params,
            auth=self.auth,
            timeout=self.timeout
        ).json()

    def paginate(self, endpoint: str, params: dict = None) -> dict:
        # source: https://docs.pro.coinbase.com/?python#pagination
        url = self.route(endpoint)

        if params is None:
            params = dict()

        while True:
            response = self.session.get(
                url,
                params=params,
                auth=self.auth,
                timeout=self.timeout
            )

            results = response.json()

            after = response.headers.get('CB-AFTER')
            before = params.get('before')
            end = not after or before

            for result in results:
                yield result

            if end:
                break

            params['after'] = response.headers['CB-AFTER']
