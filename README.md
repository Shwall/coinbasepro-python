# Coinbase Pro Python

[![Build Status](https://travis-ci.org/danpaquin/coinbasepro-python.svg?branch=master)](https://travis-ci.org/danpaquin/coinbasepro-python)

A Python 3 Wrapper Client for the [Coinbase Pro API](https://docs.pro.coinbase.com/)

- Requires Python 3.6 or greater

- Provided under MIT License by Daniel Paquin.

*Note: This library may be subtly broken or buggy.*

*NOTE: This library is a fork of the original. This library will resemble the original less over time as development continues. The API is not compatible with the original and will break your client interface. If you are here looking for the original GDAX project, you can [find it here](https://github.com/danpaquin/coinbasepro-python.git). I have left the the original `LICENSE` and `contributors.txt` files to credit the original author as well as the projects contributors.*

*The code is released under the MIT License – please take the following message to heart:*

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Benefits

- A simple to use python wrapper for both public and authenticated endpoints.
- In about 10 minutes, you could be programmatically trading on one of the
largest Bitcoin exchanges in the *world*!
- Do not worry about handling the nuances of the API with easy-to-use methods
for every API endpoint.
- Gain an advantage in the market by getting under the hood of CB Pro to learn
what and who is behind every tick.

## Under Development

- Test Scripts
- Real-Time Order Book
- Web Socket Client
- FIX API Client **Looking for assistance**

# Getting Started

This `README.md` is documentation on the syntax of the python client presented in
this repository.

See both Requests and Coinbase Pro API Documentation for full details.

- [Requests API Docs](https://docs.python-requests.org/en/master/api/)

Make sure you have a good grasp of the basic `requests` API for handling API `response` objects.

- [Coinbase Pro API Docs](https://docs.pro.coinbase.com)

You must familiarize yourself with the Official Coinbase Pro documentation in order to use it to its full potential even though this interface attempts to present a clean interface to the Coinbase Pro API.

# Install

*__NOTE__: This library conflicts with the original `coinbasepro-python` package. Make sure to remove it before installing this package to avoid package conflicts.*

- Install manually

```sh
git clone https://github.com/teleprint-me/coinbasepro-python.git
```

- Install with `pip`

```sh
pip install git+git://github.com/teleprint-me/coinbasepro-python.git
```

# API

*__WARNING__: It's recommended that you use the websocket interface instead of polling the general interface methods. It's best to reference the Coinbase Pro API Docs to see where polling is allowed, or even encouraged, in some niche cases. Polling can result in blocking, or even banning, access to the API in most other cases.*

## `cbpro.auth.Auth`

- [Authentication](https://docs.pro.coinbase.com/#authentication)

Use the `cbpro.auth.Auth` object to authenticate yourself with private endpoints.

```python
import cbpro

KEY = 'My Key'
SECRET = 'My Secret'
PASSPHRASE = 'My Passphrase'

auth = cbpro.Auth(KEY, SECRET, PASSPHRASE)
```

## `cbpro.messenger.Messenger`

- [Requests](https://docs.pro.coinbase.com/#requests) 

The `Messenger` object is a wrapper that handles making client requests a bit simpler. The `Messenger` object also handles converting a `dict` object to a json compatible object using `json.dumps` internally. 

All `Messenger` object methods return a `requests.models.Response` object. The only exception to this rule is the `Messenger.paginate` method which returns a generator.

Any objects that subscribe to the `Subscriber` interface inherit the initialization of the `Subscriber.messenger` property allowing them to effectively communicate via the same `Auth` and `requests.Session` objects without duplicating code.

This basically means **all** client interfaces inherit from the `Subscriber` object. They all share the same information without communicating directly with one another because they all have their own access to the intial `Messenger` object.

It's highly recommended to use either the `PublicClient` or the `PrivateClient` as a mediator for the `Messenger` object rather than utilizing it directly.

*__NOTE__: The `Messenger` object is __not__ a Singleton structure.*

A `Messenger` instance is passed to the `PublicClient` or `PrivateClient` objects and then shared among the related classes during instantiation of Client related object. Each instance having their own memory space and sharing the same `Messenger` instance.

Use the `cbpro.messenger.Messenger` object to communicate with the [Coinbase Pro API](https://docs.pro.coinbase.com/).

```python
import cbpro

messenger = cbpro.Messenger()
```

Use the `cbpro.auth.Auth` object to allow the `cbpro.messenger.Messenger` object
to communicate with private endpoints.

```python
KEY = 'My Key'
SECRET = 'My Secret'
PASSPHRASE = 'My Passphrase'

auth = cbpro.Auth(KEY, SECRET, PASSPHRASE)
messenger = cbpro.Messenger(auth=auth)
```

Use the [Coinbase Pro Rest API Sandbox](https://docs.pro.coinbase.com/#sandbox) for testing.

```python
url = 'https://api-public.sandbox.pro.coinbase.com'
auth = cbpro.Auth(KEY, SECRET, PASSPHRASE)
messenger = cbpro.Messenger(auth=auth, url=url)
```

### `cbpro.messenger.Messenger.paginate`

Some calls are [paginated](https://docs.pro.coinbase.com/#pagination). Multiple
calls must be made to receive the full set of data. The `Messenger` interface provides
a method for paginated endpoints. `Messenger.paginate` returns a generator which provide a clean interface for iteration and may make multiple HTTP requests behind the scenes.

The pagination options `before`, `after`, and `limit` may be supplied as keyword arguments if desired and are not necessary for typical use cases.

```python
generator = private.fills.get()
fills = list(generator)
```

One use case worth pointing out is retrieving only new data since the previous request. 

The `trade_id` is the parameter used for indexing `private.fills.get()`. If passing `before=some_trade_id`, then only fills more recent than that `trade_id` will be returned.

Note that a maximum of 100 entries will be returned when using `before` - this is a limitation set by Coinbase Pro.

```python
from itertools import islice
# Get 5 most recent fills
recent_fills = islice(private.fills.get(), 5)
# Only fetch new fills since last call by utilizing `before` parameter.
new_fills = private.fills.get(before=recent_fills[0]['trade_id'])
```

## `cbpro.public.PublicClient`

- [Coinbase Pro API Market Data](https://docs.pro.coinbase.com/#market-data)

Only some endpoints in the API are available to everyone.  The public endpoints
can be reached using `cbpro.public.PublicClient` object.

```python
cbpro.public.PublicClient(
    messenger: cbpro.messenger.Messenger
) -> cbpro.public.PublicClient
```

Example:

```python
import cbpro

messenger = cbpro.Messenger()

public = cbpro.PublicClient(messenger)

response = public.products.list()

type(response)
# <class 'requests.models.Response'>

response
# <Response [200]>

products = response.json()

type(products)
# <class 'list'>

len(products)
# 183
```

### `cbpro.public.Products`

- [Products](https://docs.pro.coinbase.com/#products)

```python
public.products
```

- [Get Products](https://docs.pro.coinbase.com/#get-products)

```python
public.products.list() -> list
```

- [Get Single Product](https://docs.pro.coinbase.com/#get-single-product)

```python
public.products.get(product_id: str) -> dict
```

Example:

```python
product_id = 'BTC-USD'

response = public.products.get(product_id)

product = response.json()

type(product)
# <class 'dict'>
```

- [Get Product Order Book](https://docs.pro.coinbase.com/#get-product-order-book)

```python
public.products.order_book(product_id: str, **params: dict) -> dict
```

Example:

```python
response = public.products.order_book(product_id)
result = response.json()

type(result)
# <class 'dict'>

result
# {
#   'bids': [['53120.08', '0.13374181', 1]], 
#   'asks': [['53120.09', '0.17580828', 4]], 
#   'sequence': 24328438628
# }
```

- [Get Product Ticker](https://docs.pro.coinbase.com/#get-product-ticker)

```python
public.product.ticker(product_id: str) -> dict
```

- [Get Trades](https://docs.pro.coinbase.com/#get-trades)

```python
public.products.trades(product_id: str) -> list
```

- [Get Historic Rates](https://docs.pro.coinbase.com/#get-historic-rates)

```python
public.products.history(product_id: str, **params: dict) -> list
```

- [Get 24hr Stats](https://docs.pro.coinbase.com/#get-24hr-stats)

```python
public.products.stats(product_id: str) -> dict
```

### `cbpro.public.Currencies`

- [Get Currencies](https://docs.pro.coinbase.com/#get-currencies)

```python
public.currencies.list() -> list
```

- [Get a currency](https://docs.pro.coinbase.com/#get-a-currency)

```python
public.currencies.get(product_id: str) -> dict
```

### `cbpro.public.Time`

- [Time](https://docs.pro.coinbase.com/#time)

```python
public.time.get() -> dict
```

## `cbpro.models.PublicModel`

Use `cbpro.models.PublicModel` to generate passable parameters easily.

```python
cbpro.models.PublicModel() -> cbpro.models.PublicModel
```

Example:

```python
# Get the order book at a specific level.
import cbpro.models

model = cbpro.models.PublicModel()

params = model.products.order_book(2)
params
# {'level': 2}

response = public.products.order_book(product_id, params=params)
response
# <Response [200]>
 
result = response.json()
type(result)
# <class 'dict'>

result
# {
#   'bids': [['53009.87', '0.35148662', 2]], 
#   'asks': [['53011.25', '0.002', 1]], 
#   'sequence': 24328747726
# }
```

### `cbpro.models.ProductsModel`

- [Order Book Parameters](https://docs.pro.coinbase.com/#get-product-order-book)

```python
model.products.order_book(level: int = None) -> dict
```

- [History Parameters](https://docs.pro.coinbase.com/#get-historic-rates)

```python
model.products.history(start: str = None, 
                       end: str = None, 
                       granularity: int = 86400) -> dict
```

## `cbpro.private.PrivateClient`

Not all API endpoints are available to everyone.
Those requiring user authentication can be reached using the `PrivateClient` object. You must setup API access within your
[Account Settings](https://pro.coinbase.com/profile/api).

The `PrivateClient` object inherits all properties from the `PublicClient`
object. You will only need to initialize one if you are planning to
integrate both into your script.

Example:

```python
import cbpro

KEY = 'My Key'
SECRET = 'My Secret'
PASSPHRASE = 'My Passphrase'

auth = cbpro.Auth(KEY, SECRET, PASSPHRASE)
messenger = cbpro.Messenger(auth=auth)
private = cbpro.PrivateClient(messenger)

response = private.products.list()

type(response)
# <class 'requests.models.Response'>

response
# <Response [200]>

products = response.json()

type(products)
# <class 'list'>

len(products)
# 183
```

### `cbpro.private.Accounts`

- [List Accounts](https://docs.pro.coinbase.com/#list-accounts)

```python
private.accounts.list() -> list
```

- [Get an Account](https://docs.pro.coinbase.com/#get-an-account)

```python
private.accounts.get(account_id: str) -> dict
```

- [Get Account History](https://docs.pro.coinbase.com/#get-account-history)

```python
# Returns generator
private.accounts.history(account_id: str) -> list
```

- [Get Holds](https://docs.pro.coinbase.com/#get-holds)

```python
# Returns generator
private.accounts.holds(account_id: str) -> list
```

### `cbpro.private.Orders`

- [Place a New Order](https://docs.pro.coinbase.com/#place-a-new-order)

```python
private.orders.post(**json: dict) -> dict
```

Example:

```python
# Buy 0.01 BTC @ 100 USD
auth_client.buy(price='100.00', #USD
               size='0.01', #BTC
               order_type='limit',
               product_id='BTC-USD')
```
```python
# Sell 0.01 BTC @ 200 USD
auth_client.sell(price='200.00', #USD
                size='0.01', #BTC
                order_type='limit',
                product_id='BTC-USD')
```
```python
# Limit order-specific method
auth_client.place_limit_order(product_id='BTC-USD', 
                              side='buy', 
                              price='200.00', 
                              size='0.01')
```
```python
# Place a market order by specifying amount of USD to use. 
# Alternatively, `size` could be used to specify quantity in BTC amount.
auth_client.place_market_order(product_id='BTC-USD', 
                               side='buy', 
                               funds='100.00')
```
```python
# Stop order. `funds` can be used instead of `size` here.
auth_client.place_stop_order(product_id='BTC-USD', 
                              stop_type='loss', 
                              price='200.00', 
                              size='0.01')
```

- [cancel_order](https://docs.pro.coinbase.com/#cancel-an-order)
```python
auth_client.cancel_order("d50ec984-77a8-460a-b958-66f114b0de9b")
```
- [cancel_all](https://docs.pro.coinbase.com/#cancel-all)
```python
auth_client.cancel_all(product_id='BTC-USD')
```

- [get_orders](https://docs.pro.coinbase.com/#list-orders) (paginated)
```python
# Returns generator:
auth_client.get_orders()
```

- [get_order](https://docs.pro.coinbase.com/#get-an-order)
```python
auth_client.get_order("d50ec984-77a8-460a-b958-66f114b0de9b")
```

- [get_fills](https://docs.pro.coinbase.com/#list-fills) (paginated)
```python
# All return generators
auth_client.get_fills()
# Get fills for a specific order
auth_client.get_fills(order_id="d50ec984-77a8-460a-b958-66f114b0de9b")
# Get fills for a specific product
auth_client.get_fills(product_id="ETH-BTC")
```

- [deposit & withdraw](https://docs.pro.coinbase.com/#depositwithdraw)
```python
depositParams = {
        'amount': '25.00', # Currency determined by account specified
        'coinbase_account_id': '60680c98bfe96c2601f27e9c'
}
auth_client.deposit(depositParams)
```
```python
# Withdraw from CB Pro into Coinbase Wallet
withdrawParams = {
        'amount': '1.00', # Currency determined by account specified
        'coinbase_account_id': '536a541fa9393bb3c7000023'
}
auth_client.withdraw(withdrawParams)
```

### WebsocketClient
If you would like to receive real-time market updates, you must subscribe to the
[websocket feed](https://docs.pro.coinbase.com/#websocket-feed).

#### Subscribe to a single product
```python
import cbpro

# Parameters are optional
wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com",
                                products="BTC-USD",
                                channels=["ticker"])
# Do other stuff...
wsClient.close()
```

#### Subscribe to multiple products
```python
import cbpro
# Parameters are optional
wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com",
                                products=["BTC-USD", "ETH-USD"],
                                channels=["ticker"])
# Do other stuff...
wsClient.close()
```

### WebsocketClient + Mongodb
The ```WebsocketClient``` now supports data gathering via MongoDB. Given a
MongoDB collection, the ```WebsocketClient``` will stream results directly into
the database collection.
```python
# import PyMongo and connect to a local, running Mongo instance
from pymongo import MongoClient
import cbpro
mongo_client = MongoClient('mongodb://localhost:27017/')

# specify the database and collection
db = mongo_client.cryptocurrency_database
BTC_collection = db.BTC_collection

# instantiate a WebsocketClient instance, with a Mongo collection as a parameter
wsClient = cbpro.WebsocketClient(url="wss://ws-feed.pro.coinbase.com", products="BTC-USD",
    mongo_collection=BTC_collection, should_print=False)
wsClient.start()
```

### WebsocketClient Methods
The ```WebsocketClient``` subscribes in a separate thread upon initialization.
There are three methods which you could overwrite (before initialization) so it
can react to the data streaming in.  The current client is a template used for
illustration purposes only.

- onOpen - called once, *immediately before* the socket connection is made, this
is where you want to add initial parameters.
- onMessage - called once for every message that arrives and accepts one
argument that contains the message of dict type.
- on_close - called once after the websocket has been closed.
- close - call this method to close the websocket connection (do not overwrite).
```python
import cbpro, time
class myWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["LTC-USD"]
        self.message_count = 0
        print("Lets count the messages!")
    def on_message(self, msg):
        self.message_count += 1
        if 'price' in msg and 'type' in msg:
            print ("Message type:", msg["type"],
                   "\t@ {:.3f}".format(float(msg["price"])))
    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()
wsClient.start()
print(wsClient.url, wsClient.products)
while (wsClient.message_count < 500):
    print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
    time.sleep(1)
wsClient.close()
```
## Testing
A test suite is under development. Tests for the authenticated client require a 
set of sandbox API credentials. To provide them, rename 
`api_config.json.example` in the tests folder to `api_config.json` and edit the 
file accordingly. To run the tests, start in the project directory and run
```
python -m pytest
```

### Real-time OrderBook
The ```OrderBook``` subscribes to a websocket and keeps a real-time record of
the orderbook for the product_id input.  Please provide your feedback for future
improvements.

```python
import cbpro, time
order_book = cbpro.OrderBook(product_id='BTC-USD')
order_book.start()
time.sleep(10)
order_book.close()
```

### Testing
Unit tests are under development using the pytest framework. Contributions are 
welcome!

To run the full test suite, in the project 
directory run:
```bash
python -m pytest
```

## Change Log
*1.1.2* **Current PyPI release**
- Refactor project for Coinbase Pro
- Major overhaul on how pagination is handled

*1.0*
- The first release that is not backwards compatible
- Refactored to follow PEP 8 Standards
- Improved Documentation

*0.3*
- Added crypto and LTC deposit & withdraw (undocumented).
- Added support for Margin trading (undocumented).
- Enhanced functionality of the WebsocketClient.
- Soft launch of the OrderBook (undocumented).
- Minor bug squashing & syntax improvements.

*0.2.2*
- Added additional API functionality such as cancelAll() and ETH withdrawal.

*0.2.1*
- Allowed ```WebsocketClient``` to operate intuitively and restructured example
workflow.

*0.2.0*
- Renamed project to GDAX-Python
- Merged Websocket updates to handle errors and reconnect.

*0.1.2*
- Updated JSON handling for increased compatibility among some users.
- Added support for payment methods, reports, and Coinbase user accounts.
- Other compatibility updates.

*0.1.1b2*
- Original PyPI Release.
