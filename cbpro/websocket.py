import json
import pymongo
import threading
import time
import websocket

import cbpro.auth
import cbpro.check
import cbpro.utils


def get_default_message() -> dict:
    return {
        'type': 'subscribe',
        'product_ids': ['BTC-USD'],
        'channels': ['ticker']
    }


def get_message(value: dict = None) -> dict:
    if value is None:
        value = get_default_message()

    cbpro.check.websocket_params(value)

    return value


class WebsocketHeader(object):
    def __init__(self,
                 key: str,
                 secret: str,
                 passphrase: str) -> None:

        self.token = cbpro.auth.Token(key, secret, passphrase)

    def __call__(self) -> dict:
        timestamp = cbpro.auth.get_timestamp()
        message = f'{timestamp}GET/users/self/verify'
        b64signature = cbpro.auth.get_b64signature(message, self.token)

        return {
            'signature': b64signature,
            'key': self.token.key,
            'passphrase': self.token.passphrase,
            'timestamp': timestamp
        }


class WebsocketStream(object):
    def __init__(self,
                 header: WebsocketHeader = None,
                 timeout: int = None,
                 traceable: bool = False) -> None:

        self.header = header
        self.timeout = 30 if timeout is None else timeout
        self.traceable = traceable
        self.url = 'wss://ws-feed.pro.coinbase.com'
        self.connection = None

    @property
    def connected(self):
        if self.connection and self.connection.connected:
            return True
        return False

    def connect(self) -> None:
        header = None if self.header is None else self.header()
        websocket.enableTrace(self.traceable)
        self.connection = websocket.create_connection(
            url=self.url, header=header
        )

    def send(self, params: dict) -> None:
        if self.connected:
            payload = json.dumps(params)
            self.connection.send(payload)

    def receive(self) -> dict:
        if self.connected:
            payload = self.connection.recv()
            if payload:
                return json.loads(payload)
        return dict()

    def ping(self) -> None:
        payload = 'keepalive'
        while self.connected:
            if self.traceable:
                print(f'[Ping] {payload} [Timeout] {self.timeout}s')
            self.connection.ping(payload)
            time.sleep(self.timeout)

    def disconnect(self) -> None:
        if self.connected:
            self.connection.close()


class WebsocketEvent(object):
    def on_error(self, value: str) -> None:
        print(f'[Exception] {value}\n')

    def on_start(self):
        print(f'[Start] thread {threading.get_native_id()}')
        time.sleep(1)

    def on_run(self):
        print(f'[Run] {threading.active_count()} active threads')
        time.sleep(1)

    def on_stop(self):
        print(f'[Stop] thread {threading.get_native_id()}')

    def on_listen(self, client: object, value: dict) -> None:
        self.on_response(value)
        self.on_collection(client, value)

    def on_response(self, value: dict) -> None:
        print(f'[Response] {value}')
        time.sleep(1)

    def on_collection(self, collection: object, value: dict) -> None:
        if collection:
            collection.insert_one(value)


class WebsocketClient(object):
    def __init__(self,
                 stream: WebsocketStream,
                 event: WebsocketEvent = None,
                 collection: pymongo.collection.Collection = None) -> None:

        self.stream = stream
        self.collection = collection
        self.running = False
        self.thread = None
        self.keepalive = None
        self.event = WebsocketEvent() if event is None else event

    def listen(self) -> None:
        while self.running:
            message = self.stream.receive()
            if message:
                self.event.on_listen(self.collection, message)

    def start(self, value: dict) -> None:
        self.event.on_start()
        self.running = True
        self.stream.connect()
        self.stream.send(value)
        self.listen()

    def run(self, params: dict) -> None:
        self.event.on_run()
        self.thread = threading.Thread(target=self.start, args=(params,))
        self.thread.start()

    def stop(self) -> None:
        self.event.on_stop()
        self.running = False
        self.stream.disconnect()
        self.thread.join()


def websocket_client(key: str = None,
                     secret: str = None,
                     passphrase: str = None,
                     event: WebsocketEvent = None,
                     collection: pymongo.collection.Collection = None,
                     traceable: bool = False) -> WebsocketClient:

    header = None

    if key and secret and passphrase:
        header = WebsocketHeader(key, secret, passphrase)

    stream = WebsocketStream(header=header, traceable=traceable)

    return WebsocketClient(stream, event, collection)