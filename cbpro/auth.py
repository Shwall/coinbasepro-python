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
#
# source: https://docs.pro.coinbase.com/?python#signing-a-message
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


class Payload(object):
    def __init__(self, request: PreparedRequest) -> None:
        self.__request = request
        self.__timestamp = str(time.time())

    @property
    def timestamp(self) -> str:
        return self.__timestamp

    @property
    def message(self) -> bytes:
        method = self.__request.method
        path = self.__request.path_url
        body = self.__request.body or ''
        timestamp = self.__timestamp
        return f'{timestamp}{method}{path}{body}'.encode('ascii')


class Header(object):
    def __init__(self, token: Token, payload: Payload) -> None:
        hmac_key = base64.b64decode(token.secret)
        signature = hmac.new(
            hmac_key, payload.message, hashlib.sha256)

        self.__token = token
        self.__payload = payload
        self.__signature = base64.b64encode(
            signature.digest()).decode('utf-8')

    @property
    def content(self) -> dict:
        return {
            'Content-Type': 'Application/JSON',
            'CB-ACCESS-SIGN': self.__signature,
            'CB-ACCESS-TIMESTAMP': self.__payload.timestamp,
            'CB-ACCESS-KEY': self.__token.key,
            'CB-ACCESS-PASSPHRASE': self.__token.passphrase
        }


class Auth(AuthBase):
    def __init__(self, key: str, secret: str, passphrase: str) -> None:
        self.__token = Token(key, secret, passphrase)

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        payload = Payload(request)
        header = Header(self.__token, payload)
        request.headers.update(header.content)
        return request
