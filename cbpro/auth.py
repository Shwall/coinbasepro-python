#
# source: https://docs.pro.coinbase.com/?python#signing-a-message
#
# NOTE:
#   Your timestamp must be within 30 seconds of the api service time or your
#   request will be considered expired and rejected. We recommend using the
#   time endpoint to query for the API server time if you believe there many
#   be time skew between your server and the API servers.
#
# source: https://docs.pro.coinbase.com/?python#selecting-a-timestamp
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


def get_timestamp() -> str:
    return str(time.time())


def get_request_body(request: PreparedRequest) -> str:
    return '' if request.body is None else request.body.decode('utf-8')


def get_message(timestamp: str, request: PreparedRequest) -> str:
    body = get_request_body(request)
    return f'{timestamp}{request.method}{request.path_url}{body}'


def get_b64signature(message: str, token: Token) -> bytes:
    key = base64.b64decode(token.secret)
    msg = message.encode('ascii')
    sig = hmac.new(key, msg, hashlib.sha256)
    digest = sig.digest()
    b64signature = base64.b64encode(digest)
    return b64signature.decode('utf-8')


def get_headers(timestamp: str, b64signature: bytes, token: Token) -> dict:
    return {
        'CB-ACCESS-SIGN': b64signature,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-KEY': token.key,
        'CB-ACCESS-PASSPHRASE': token.passphrase,
        'Content-Type': 'application/json'
    }


class Auth(AuthBase):
    def __init__(self, key, secret, passphrase) -> None:
        self.token = Token(key, secret, passphrase)

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        timestamp = get_timestamp()
        message = get_message(timestamp, request)
        b64signature = get_b64signature(message, self.token)
        headers = get_headers(timestamp, b64signature, self.token)
        request.headers.update(headers)
        return request
