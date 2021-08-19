import requests
import time

import cbpro.auth


__sleep__ = 0.275


class Messenger(object):
    def __init__(self,
                 auth: cbpro.auth.Auth = None,
                 url: str = None,
                 timeout: int = None) -> None:

        api = 'https://api.pro.coinbase.com'
        self.auth = auth
        self.url = api if url is None else url.rstrip('/')
        self.timeout = 30 if timeout is None else timeout
        self.session = requests.Session()

    def route(self, endpoint: str) -> str:
        return f'{self.url}{endpoint}'

    def get(self, endpoint: str, params: dict = None) -> dict:
        time.sleep(__sleep__)
        url = self.route(endpoint)
        response = self.session.get(
            url,
            params=params,
            auth=self.auth,
            timeout=self.timeout
        )
        return response.json()

    def post(self,
             endpoint: str,
             params: dict = None,
             json: dict = None) -> dict:

        time.sleep(__sleep__)
        response = self.session.post(
            url=self.route(endpoint),
            params=params,
            json=json,
            auth=self.auth,
            timeout=self.timeout
        )

        return response.json()

    def delete(self, endpoint: str, **kwargs: dict) -> dict:
        time.sleep(__sleep__)
        url = self.route(endpoint)
        response = self.session.delete(
            url,
            auth=self.auth,
            timeout=self.timeout,
            **kwargs
        )
        return response.json()

    def request(self,
                method: str,
                endpoint: str,
                params: dict = None,
                json: dict = None) -> dict:

        time.sleep(__sleep__)
        url = self.route(endpoint)
        response = self.session.request(
            method,
            url,
            json=json,
            params=params,
            auth=self.auth,
            timeout=self.timeout
        )
        return response.json()

    def paginate(self, endpoint: str, params: dict = None) -> object:
        # source: https://docs.pro.coinbase.com/?python#pagination
        url = self.route(endpoint)
        if params is None:
            params = dict()
        while True:
            time.sleep(__sleep__)
            response = self.session.get(
                url,
                params=params,
                auth=self.auth,
                timeout=self.timeout
            )
            results = response.json()
            if response.status_code != 200:
                return results
            for result in results:
                yield result
            after = response.headers.get('CB-AFTER')
            before = params.get('before')
            end = not after or before
            if end:
                break
            params['after'] = response.headers['CB-AFTER']


class Subscriber(object):
    def __init__(self, messenger: Messenger) -> None:
        self.__messenger = messenger

    @property
    def messenger(self) -> Messenger:
        return self.__messenger
