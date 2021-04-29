#
# source: https://docs.pro.coinbase.com/?python#signing-a-message
#
from requests.auth import AuthBase
from requests.models import PreparedRequest

import base64
import hmac
import hashlib
import time


class Token(object):
    def __init__(self, key: str, secret: str, passphrase: str) -> None:
        self.__key = key
        self.__secret = secret
        self.__passphrase = passphrase

    @property
    def key(self) -> str:
        return self.__key

    @property
    def secret(self) -> str:
        return self.__secret

    @property
    def passphrase(self) -> str:
        return self.__passphrase


# Your timestamp must be within 30 seconds of the api service time or your
# request will be considered expired and rejected. We recommend using the
# time endpoint to query for the API server time if you believe there many
# be time skew between your server and the API servers.
# source: https://docs.pro.coinbase.com/?python#selecting-a-timestamp
class Payload(object):
    def __init__(self, request: PreparedRequest) -> None:
        self.__request = request
        self.__timestamp = str(time.time())

    @property
    def request(self):
        return self.__request

    @property
    def timestamp(self) -> str:
        return self.__timestamp

    @property
    def message(self) -> bytes:
        method = self.request.method
        path = self.request.path_url
        body = self.request.body or ''
        timestamp = self.timestamp
        return f'{timestamp}{method}{path}{body}'.encode('ascii')


class Header(object):
    def __init__(self, token: Token, payload: Payload) -> None:
        self.__token = token
        self.__payload = payload

    @property
    def token(self):
        return self.__token

    @property
    def payload(self):
        return self.__payload

    @property
    def signature(self):
        key = base64.b64decode(self.token.secret)
        signature = hmac.new(
            key, self.payload.message, hashlib.sha256
        )
        digest = signature.digest()
        return base64.b64encode(digest).decode('utf-8')

    @property
    def content(self) -> dict:
        return {
            'Content-Type': 'Application/JSON',
            'CB-ACCESS-SIGN': self.signature,
            'CB-ACCESS-TIMESTAMP': self.payload.timestamp,
            'CB-ACCESS-KEY': self.token.key,
            'CB-ACCESS-PASSPHRASE': self.token.passphrase
        }


class Auth(AuthBase):
    def __init__(self, key: str, secret: str, passphrase: str) -> None:
        self.__token = Token(key, secret, passphrase)

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        payload = Payload(request)
        header = Header(self.token, payload)
        request.headers.update(header.content)
        return request

    @property
    def token(self):
        return self.__token
