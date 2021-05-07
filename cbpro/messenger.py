from json import dumps

import requests
import cbpro.auth


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
        url = self.route(endpoint)

        return self.session.get(
            url,
            params=params,
            auth=self.auth,
            timeout=self.timeout
        ).json()

    def post(self,
             endpoint: str,
             params: dict = None,
             json: dict = None) -> dict:

        url = self.route(endpoint)
        json = json if json is None else dumps(json)

        return self.session.post(
            url,
            params=params,
            json=json,
            auth=self.auth,
            timeout=self.timeout
        ).json()

    def delete(self, endpoint: str, **kwargs: dict) -> dict:
        url = self.route(endpoint)

        return self.session.delete(
            url,
            auth=self.auth,
            timeout=self.timeout,
            **kwargs
        ).json()

    def request(self,
                method: str,
                endpoint: str,
                params: dict = None,
                json: dict = None) -> dict:

        url = self.route(endpoint)
        json = json if json is None else dumps(json)

        return self.session.request(
            method,
            url,
            json=json,
            params=params,
            auth=self.auth,
            timeout=self.timeout
        ).json()

    def paginate(self, endpoint: str, params: dict = None) -> object:
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
